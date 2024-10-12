import streamlit as st
from PIL import Image
import pytesseract
import json
import time
from openai import OpenAI
import APIKeys
from APIKeys import *

client = OpenAI(api_key=APIKeys.OPEN_AI_API_KEY)


def parse_rec(rec):
    try:
        prompt = "I am passing in the text from a Renewable Energy Certificate (REC). Parse the text and output in the JSON format below:\n" \
                 "{\"certifier\": \"the name of the company/organization that certified this REC\", \"user\": \"the name of the organization/user the REC was awarded to\", \"co2\": \"the number of metric tonnes of CO2 that was offset\"}.\n" \
                 "Here is the text from the REC:\\" + rec + "\n"
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
        return ''
    except Exception as e:
        return f"Error: {e}"


def navigate_to(page):
    st.session_state['page'] = page


st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
st.sidebar.button("Dashboard", on_click=navigate_to, args=("consumer_dash",))
st.sidebar.button("Upload Contract", on_click=navigate_to, args=("upload_rec",))

if 'file_processed' not in st.session_state:
    st.session_state['file_processed'] = False
if 'parsed_rec' not in st.session_state:
    st.session_state['parsed_rec'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'consumer_dash'

if st.session_state['page'] == 'consumer_dash':
    st.title("Contract Management Dashboard")

    # Create two columns: Active Contracts and Completed Orders
    col1, col2 = st.columns(2)

    # Left column: Active Contracts
    with col1:
        st.header("Active Contracts")

        # Example of an active contract
        st.subheader("Date: October 10, 2024")
        st.text("Tons of CO2: 100")
        st.text("Companies: Amazon, Walmart, Apple")

        # Add more contracts as needed
        st.subheader("Date: October 11, 2024")
        st.text("Tons of CO2: 250")
        st.text("Companies: Netflix, Airbnb")

        st.subheader("Date: October 12, 2024")
        st.text("Tons of CO2: 300")
        st.text("Companies: Nike, Samsung")

    # Right column: Completed Orders
    with col2:
        st.header("Completed Orders")

        # Example of a completed order
        st.subheader("Date Completed: October 9, 2024")
        st.text("Tons of CO2: 150")
        st.text("Money Earned: $10,000")
        st.text("Fulfilled by: Apple")

        # Add more completed orders as needed
        st.subheader("Date Completed: October 8, 2024")
        st.text("Tons of CO2: 200")
        st.text("Money Earned: $15,000")
        st.text("Fulfilled by: Amazon")

        st.subheader("Date Completed: October 7, 2024")
        st.text("Tons of CO2: 100")
        st.text("Money Earned: $5,000")
        st.text("Fulfilled by: Walmart")


elif st.session_state['page'] == 'upload_rec':
    # Title of the app
    st.title('Upload Clean Energy Contract')

    # Custom CSS for borders and search bar/button styles
    st.markdown("""
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
            .full-width-search {
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True)

    # Create two columns for layout with borders
    col1, col2 = st.columns([1, 1], gap="medium")

    # File uploader widget in the first column with border
    with col1:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)

        st.markdown("""
            <style>
            .select-companies-label {
                font-size: 24px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)

        # Display the label with the custom class
        st.markdown('<div class="select-companies-label">Upload your Renewable Energy Certificate (REC):</div>',
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Renewable Energy Certificate (REC)', use_column_width=True)

            if not st.session_state['file_processed']:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                extracted_text = pytesseract.image_to_string(image)
                parsed_rec = parse_rec(extracted_text)
                st.session_state['parsed_rec'] = parsed_rec
            else:
                parsed_rec = st.session_state['parsed_rec']

            st.text('Certifier: ' + parsed_rec['certifier'])
            st.text('Awardee: ' + parsed_rec['user'])
            st.text('CO₂ Offset (metric tonnes): ' + parsed_rec['co2'])

            if not st.session_state['file_processed']:
                with st.spinner('Processing...'):
                    time.sleep(2)

            if parsed_rec['co2'] == '250':
                st.success('REC Verified')
            else:
                st.error('REC Invalid')
            st.session_state['file_processed'] = True

        st.markdown('</div>', unsafe_allow_html=True)

    # Company selection in the second column with border
    with col2:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)

        st.markdown("""
                <style>
                .select-companies-label {
                    font-size: 24px;
                    font-weight: bold;
                }
                </style>
                """, unsafe_allow_html=True)

        # Display the label with the custom class
        st.markdown('<div class="select-companies-label">Select Companies:</div>',
                    unsafe_allow_html=True)

        company_logos = {
            "Amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
            "Walmart": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg",
            "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
            "Netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
            "Airbnb": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_Bélo.svg",
            "Nike": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg",
            "Adidas": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg",
            "Samsung": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
        }

        st.markdown("""
            <style>
            .stButton button {
                width: 100%;
            }
            </style>
            """, unsafe_allow_html=True)

        # Form with full-width submit button
        with st.form(key='search_form'):
            search_query = st.text_input("Search for a company:\n")
            submitted = st.form_submit_button("Search")

        filtered_companies = {k: v for k, v in company_logos.items() if search_query.lower() in k.lower()}

        selected_companies = []
        for company, logo_url in filtered_companies.items():
            col_checkbox, col_image, col_name = st.columns([1, 1, 5])
            with col_checkbox:
                is_selected = st.checkbox("", key=company)
                selected_companies.append((company, is_selected))
            with col_image:
                st.image(logo_url, width=40)
            with col_name:
                st.markdown(f'<div class="company-name">{company}</div>', unsafe_allow_html=True)

        selected_companies = [company for company, selected in selected_companies if selected]
        if selected_companies:
            st.write("You selected:")
            for company in selected_companies:
                st.write(f"- {company}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <style>
        .full-width-button {
            display: block;
            width: 100%;
            color: white;
            background-color: #28a745;
            border: none;
            padding: 0.75em;
            font-size: 1em;
            text-align: center;
            cursor: pointer;
            border-radius: 5px;
        }
        .full-width-button:hover {
            background-color: #218838;
        }
        </style>
        """, unsafe_allow_html=True)

    # Create a button with custom styles
    if st.button('Upload Contract', key='upload contract'):
        # Code to run when the button is pressed
        st.session_state['page'] = 'consumer_dash'
