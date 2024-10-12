import time

import streamlit as st
import pytesseract
from PIL import Image

from navigation import make_sidebar
from pages.consumer_sell import parse_rec

make_sidebar()

# Title of the app
st.title("Upload Clean Energy Contract")

if 'company_page' not in st.session_state:
    st.session_state['company_page'] = 0

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Create two columns for layout with borders
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
            image, caption="Renewable Energy Certificate (REC)", use_column_width=True
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

    companies_per_page = 5
    total_companies = len(filtered_companies)
    page_count = (total_companies - 1) // companies_per_page + 1  # Total number of pages

    # Get the current batch of companies to display
    start_idx = st.session_state['company_page'] * companies_per_page
    end_idx = min(start_idx + companies_per_page, total_companies)
    current_companies = list(filtered_companies.items())[start_idx:end_idx]

    for company, logo_url in current_companies:
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
                f'<div class="company-name">${100}</div>', unsafe_allow_html=True
            )

    st.markdown("""
        <style>
        .custom-button {
            # background-color: transparent; /* Green */
            color: white;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            transition-duration: 0.4s;
            text-color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    side, col1, col2, col3, side2 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.markdown('<a href="#" class="custom-button">Prev</a>', unsafe_allow_html=True) and st.session_state['company_page'] > 0:
            st.session_state['company_page'] -= 1
    with col3:
        if st.markdown('<a href="#" class="custom-button">Next</a>', unsafe_allow_html=True) and st.session_state['company_page'] < page_count - 1:
            st.session_state['company_page'] += 1

    st.write(st.session_state['company_page'])
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
    """,
    unsafe_allow_html=True,
)

if st.markdown(
    '<button class="full-width-button">Submit</button>', unsafe_allow_html=True
):
    # Code to run when the button is pressed
    st.write("upload with blockchain")
