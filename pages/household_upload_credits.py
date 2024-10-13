import time
import json
from datetime import datetime
from PIL import Image
import pytesseract
import streamlit as st
from openai import OpenAI
from APIKeys import OPEN_AI_API_KEY
from navigation import make_sidebar

# Initialize Sidebar and MongoDB Connection
make_sidebar()
db = st.session_state.dbClient["hackharvard"]
household_rec_collection = db["household_rec"]
company_collection = db["company"]

# Initialize OpenAI Client
client = OpenAI(api_key=OPEN_AI_API_KEY)

# Title of the App
st.title("Sell Clean Energy Contract (CEC)")

# Session State Initialization
st.session_state["file_processed"] = False
st.session_state["parsed_rec"] = {"co2": 0, "user": "test", "certifier": "test"}
st.session_state["submitted"] = False


# Function to Parse the REC
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


col1, col2 = st.columns([1, 1], gap="large")

# File Uploader Widget in Column 1
with col1:

    st.write("### Upload your Renewable Energy Certificate (REC):")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Renewable Energy Certificate (REC)",
            use_column_width=True,
        )

        if not st.session_state["file_processed"]:
            time.sleep(2)
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )
            extracted_text = pytesseract.image_to_string(image)
            parsed_rec = parse_rec(extracted_text)
            st.session_state["parsed_rec"] = parsed_rec
        else:
            parsed_rec = st.session_state["parsed_rec"]

        st.text(f"Certifier: {parsed_rec['certifier']}")
        st.text(f"Awardee: {parsed_rec['user']}")
        st.text(f"CO₂ Offset (metric tonnes): {parsed_rec['co2']}")

        if not st.session_state["file_processed"]:
            with st.spinner("Processing..."):
                time.sleep(2)

        if parsed_rec["co2"] == "250":
            st.session_state["file_processed"] = True
            st.success("REC Verified")
        else:
            st.error("REC Invalid")

# Company Selection in Column 2
if st.session_state["file_processed"] and parsed_rec["co2"] == "250":
    with col2:

        st.write("### Select company to trade with: ")
        company_logos = {}
        company_prices = {}
        company_data = list(company_collection.find())

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

        # Form with Search Field
        with st.form(key="search_form"):
            search_query = st.text_input("Search for a company:\n")
            submitted = st.form_submit_button("Search")

        filtered_companies = {
            k: v for k, v in company_logos.items() if search_query.lower() in k.lower()
        }

        selected_companies = []
        col_name, col_price, col_checkbox = st.columns([2, 2, 1])
        with col_name:
            st.write("#### Company")
        with col_price:
            st.write("#### Price per Credit")

        for company, logo_url in filtered_companies.items():
            col_image, col_price, col_checkbox = st.columns([2, 2, 1])
            with col_checkbox:
                is_selected = st.checkbox("", key=company)
                selected_companies.append((company, is_selected))
            with col_image:
                st.image(
                    logo_url,
                    width=120,
                )
            with col_price:
                st.write(f"##### ${company_prices[company]}")

        selected_companies = [
            company for company, selected in selected_companies if selected
        ]

_, submit_col, _ = st.columns([2, 1, 2])
if (
    st.session_state["file_processed"]
    and st.session_state["parsed_rec"]["co2"] == "250"
    and selected_companies
):
    with submit_col:
        if st.button("Transfer Contract"):
            with st.spinner("Transferring..."):
                time.sleep(2)
                parsed_rec = st.session_state["parsed_rec"]
                contract = {
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": time.time(),
                    "traded_to": selected_companies[0],
                    "company_credits_earned": int(
                        company_prices[selected_companies[0]]
                    ),
                    "user": st.session_state.username,
                    "REC_credits_traded": int(parsed_rec["co2"]),
                }
                household_rec_collection.insert_one(contract)

            st.session_state["submitted"] = True
            st.session_state["file_processed"] = False
            st.session_state["parsed_rec"] = {
                "co2": 0,
                "user": "test",
                "certifier": "test",
            }

            st.success("CEC Uploaded Successfully.", icon="🚀")
            time.sleep(1)
            st.switch_page("pages/household_transaction_history.py")
