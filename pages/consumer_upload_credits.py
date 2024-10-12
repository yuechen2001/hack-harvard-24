import time

from openai import OpenAI
import streamlit as st
import pytesseract
from PIL import Image
import json
import pyautogui

from APIKeys import OPEN_AI_API_KEY, MONGO_URI
from navigation import make_sidebar
from datetime import datetime

from pages.consumer_transaction_history import get_data

make_sidebar()

db = st.session_state.dbClient["hackharvard"]
rec_collection = db["consumer_rec"]
company_collection = db["company"]

# Title of the app
st.title("Upload Clean Energy Contract")

client = OpenAI(api_key=OPEN_AI_API_KEY)
if "file_processed" not in st.session_state:
    st.session_state["file_processed"] = False
if "parsed_rec" not in st.session_state:
    st.session_state["parsed_rec"] = {"co2": 0, "user": "test", "certifier": "test"}
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# Custom CSS for borders and search bar/button styles
st.markdown(
    """
    <style>
        .stColumn {
            # border: 2px solid #f0f0f0;
            padding: 20px;
            border-radius: 5px;
        }
        .stTextInput input, .stButton button {
            width: 100%;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .stButton button {
            background-color: #28a745;
            color: white;
        }
        .stButton button:hover {
            background-color: #218838;
        }
        .company-name {
            font-size: 20px;
        }
        .company-titles {
            font-size: 24px;
            font-weight: bold;
        }
        .full-width-search {
            width: 100%;
        }
        .stToast {  
        background-color: #4CAF50; 
        color: white;
        padding: 20px;
        border-radius: 5px;
        font-size: 64px;
        text-align: center;
        width: 100%;
        max-width: 600px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def parse_rec(rec):
    try:
        prompt = (
            "I am passing in the text from a Renewable Energy Certificate (REC). Parse the text and output in the JSON format below:\n"
            '{"certifier": "the name of the company/organization that certified this REC", "user": "the name of the organization/user the REC was awarded to", "co2": "the number of metric tonnes of CO2 that was offset"}.\n'
            "Here is the text from the REC:\\" + rec + "\n"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.4,
        )
        if response.choices[0].message.content is not None:
            return json.loads(response.choices[0].message.content)
        return ""
    except Exception as e:
        return f"Error: {e}"


if st.session_state["submitted"]:
    st.text(
        "Congratulations! Your clean energy contract has been uploaded and fulfilled."
    )
    st.session_state["submitted"] = False
else:
    col1, col2 = st.columns([1, 1], gap="medium")

    # File uploader widget in the first column with border
    with col1:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)

        st.markdown(
            """
            <style>
            .select-companies-label {
                font-size: 24px;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Display the label with the custom class
        st.markdown(
            '<div class="select-companies-label">Upload your Renewable Energy Certificate (REC):</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(
                image,
                caption="Renewable Energy Certificate (REC)",
                use_column_width=True,
            )

            if not st.session_state["file_processed"]:
                pytesseract.pytesseract.tesseract_cmd = (
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                )
                extracted_text = pytesseract.image_to_string(image)
                parsed_rec = parse_rec(extracted_text)
                st.session_state["parsed_rec"] = parsed_rec
            else:
                parsed_rec = st.session_state["parsed_rec"]

            st.text("Certifier: " + parsed_rec["certifier"])
            st.text("Awardee: " + parsed_rec["user"])
            st.text("CO₂ Offset (metric tonnes): " + parsed_rec["co2"])

            if not st.session_state["file_processed"]:
                with st.spinner("Processing..."):
                    time.sleep(2)

            if parsed_rec["co2"] == "250":
                st.success("REC Verified")
            else:
                st.error("REC Invalid")
            st.session_state["file_processed"] = True

        st.markdown("</div>", unsafe_allow_html=True)

    # Company selection in the second column with border
    with col2:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)

        st.markdown(
            """
                <style>
                .select-companies-label {
                    font-size: 24px;
                    font-weight: bold;
                }
                </style>
                """,
            unsafe_allow_html=True,
        )

        # Display the label with the custom class
        st.markdown(
            '<div class="select-companies-label">Select Companies:</div>',
            unsafe_allow_html=True,
        )

        company_logos = {}
        company_prices = {}
        company_data = list(company_collection.find({}, {}))

        for c in company_data:
            if c["carbon_balance"] < 0:
                company_logos[c["name"]] = c["image_url"]
                company_prices[c["name"]] = c["price_per_REC_credit"]

        sorted_companies = sorted(company_prices, key=company_prices.get, reverse=True)
        company_logos = {
            company: company_logos[company] for company in sorted_companies
        }
        company_prices = {
            company: company_prices[company] for company in sorted_companies
        }

        st.markdown(
            """
            <style>
            .stButton button {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Form with full-width submit button
        with st.form(key="search_form"):
            search_query = st.text_input("Search for a company:\n")
            submitted = st.form_submit_button("Search")

        filtered_companies = {
            k: v for k, v in company_logos.items() if search_query.lower() in k.lower()
        }

        selected_companies = []
        col_name, col_price, col_checkbox = st.columns([3, 1, 1])
        with col_name:
            st.markdown(
                f'<div class="company-titles">Company</div>', unsafe_allow_html=True
            )
        with col_price:
            st.markdown(
                f'<div class="company-titles">Price</div>', unsafe_allow_html=True
            )

        for company, logo_url in filtered_companies.items():
            col_image, col_name, col_price, col_checkbox = st.columns([1, 2, 1, 1])
            with col_checkbox:
                is_selected = st.checkbox("", key=company)
                selected_companies.append((company, is_selected))
            with col_image:
                st.image(logo_url, width=40)
            with col_name:
                st.markdown(
                    f'<div class="company-name">{company}</div>', unsafe_allow_html=True
                )
            with col_price:
                st.markdown(
                    f'<div class="company-name">${company_prices[company]}</div>',
                    unsafe_allow_html=True,
                )

        selected_companies = [
            company for company, selected in selected_companies if selected
        ]
        if selected_companies:
            st.write("You selected:")
            for company in selected_companies:
                st.write(f"- {company}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .full-width-button {
            display: block;
            width: 100%;
            height: 50px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 20px;
        }
        .full-width-button:hover {
            background-color: #45a049;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    if st.button("Submit"):
        with st.spinner("Transacting..."):
            # Code to run when the button is pressed
            parsed_rec = st.session_state["parsed_rec"]
            contract = {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": time.time(),
                "traded_to": selected_companies[0],
                "company_credits_earned": int(company_prices[selected_companies[0]]),
                "user": st.session_state.username + "@gmail.com",
                "REC_credits_traded": int(parsed_rec["co2"]),
            }
            time.sleep(2)
            rec_collection.insert_one(contract)

        st.toast("Contract uploaded successfully!", icon="🚀")
        time.sleep(2)
        st.switch_page("pages/consumer_transaction_history.py")
