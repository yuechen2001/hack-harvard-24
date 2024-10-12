from openai import OpenAI
import requests
import streamlit as st
from PIL import Image
import pytesseract

import APIKeys
from APIKeys import *

client = OpenAI(api_key=APIKeys.OPEN_AI_API_KEY)


# Function to check if logo is valid
def is_logo_valid(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


def parse_rec(rec):
    try:
        prompt = "I am passing in the text from a Renewable Energy Certificate (REC). Parse the text and output in the JSON format below:\n" \
                 "{\"certifier\": \"the name of the company/organization that certified this REC\", \"user\": \"the name of the organization/user the REC was awarded to\", \"co2\": \"the number of metric tonnes of CO2 that was offset\"}.\n" \
                 "Here is the text from the REC:\\" + rec + "\n"
        response = client.chat.completions.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" or any other supported model
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,  # Adjust this for the length of the response
            n=1,
            stop=None,
            temperature=0.4,  # Adjust the creativity (0.0-1.0)
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


# Title of the app
st.title('Image Upload Example')

# Create two columns for layout
col1, col2 = st.columns(2)

# File uploader widget in the first column
with col1:
    uploaded_file = st.file_uploader("Choose an image for OCR...", type=["jpg", "jpeg", "png"])

    # Check if an image file is uploaded
    if uploaded_file is not None:
        # Open the uploaded image file
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("Image uploaded successfully!")

        # Perform OCR using pytesseract
        st.write("Extracting text from image...")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        extracted_text = pytesseract.image_to_string(image)

        parsed_rec = parse_rec(extracted_text)
        st.text(parsed_rec)
    else:
        st.write("Upload an image file to extract text from.")

# Add checkboxes for company selection in the second column with logos and search bar
with col2:
    st.write("Select companies:")

    # Dictionary with company names as keys and their logo URLs as values
    company_logos = {
        "Amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "Walmart": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg",
        "Target": "https://upload.wikimedia.org/wikipedia/commons/8/88/Target_logo.svg",
        "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
        "Google": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
        "Facebook": "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg",
        "Microsoft": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
        "Tesla": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Tesla_Motors.svg",
        "Netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
        "Uber": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.svg",
        "Airbnb": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_Bélo.svg",
        "Nike": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg",
        "Adidas": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg",
        "Coca-Cola": "https://upload.wikimedia.org/wikipedia/commons/1/19/Coca-Cola_logo.svg",
        "Pepsi": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Pepsi_logo.svg",
        "Samsung": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
        "Sony": "https://upload.wikimedia.org/wikipedia/commons/2/20/Sony_logo.svg",
        "Disney": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Disney_wordmark.svg",
        "McDonald's": "https://upload.wikimedia.org/wikipedia/commons/4/4e/McDonald%27s_Golden_Arches.svg",
        "Starbucks": "https://upload.wikimedia.org/wikipedia/commons/4/45/Starbucks_Corporation_Logo_2011.svg"
    }

    # Wrap search bar in a form for auto-refresh
    with st.form(key='search_form'):
        search_query = st.text_input("Search for a company:")
        submitted = st.form_submit_button("Search")

    # Filter companies based on search query (case insensitive)
    filtered_companies = {k: v for k, v in company_logos.items() if
                          search_query.lower() in k.lower() and is_logo_valid(v)}

    # Create a checkbox, logo, and name for each filtered company
    selected_companies = []
    for company, logo_url in filtered_companies.items():
        # Display the checkbox, logo, and company name in one row
        col_checkbox, col_image, col_name = st.columns([1, 1, 4])
        with col_checkbox:
            is_selected = st.checkbox("", key=company)
            selected_companies.append((company, is_selected))
        with col_image:
            st.image(logo_url, width=40)
        with col_name:
            st.write(company)

    # Display selected companies
    selected_companies = [company for company, selected in selected_companies if selected]
    if selected_companies:
        st.write("You selected:")
        for company in selected_companies:
            st.write(f"- {company}")
