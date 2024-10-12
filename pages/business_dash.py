import streamlit as st
import pandas as pd
import numpy as np
from navigation import make_sidebar

make_sidebar()


def get_transaction_data():
    db = st.session_state.dbClient["hackharvard"]
    items = (
        db.business_rec.find({"traded_from": st.session_state.username + "@gmail.com"})
        .sort([("timestamp", -1)])
        .limit(10)
    )
    items = list(items)
    return items


def get_business_data():
    db = st.session_state.dbClient["hackharvard"]
    items = db.company.find({"name": st.session_state.username})
    return items[0]


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
        .smaller-words {
            font-size: 24px;
            font-weight: normal;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "market_price" not in st.session_state:
    st.session_state["market_price"] = 100  # Find actual market price with block chain

business = get_business_data()
company_name = business["name"]
company_logo_url = business["image_url"]  # Replace with your actual logo URL


# Custom CSS to add a white background to the logo container and grey box for text
st.markdown(
    """
    <style>
    .logo-container {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }
    .logo-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .grey-box {
        background-color: #333333;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create two columns: one for the logo and one for the price
col1, col2 = st.columns(2)

# Display the company logo in the first column (on the left) with a white background
with col1:
    st.markdown(
        f"""
        <div class="logo-container">
            <img class = "logo-image" src="{company_logo_url}" alt="{company_name} Logo" width="400">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display the credit price in the second column (on the right) wrapped in a grey box
with col2:
    st.markdown(
        f"""
        <div class="grey-box">
            <h2>Company Name: {company_name}</h2>
            <h2 class="smaller-words">Current Carbon Balance: {business['carbon_balance']} </h2>
            <h2 class="smaller-words">Current Wallet Value: {business['money']} </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Completed orders data
data = get_transaction_data()

# Remove '_id' field from each document
for document in data:
    document.pop("_id", None)
    document.pop("traded_from", None)
    document.pop("timestamp", None)

# Convert to DataFrame (removing the _id field)
df = pd.DataFrame(data)
# Rename columns to more readable names
df.rename(
    columns={
        "datetime": "Date & Time",
        "traded_to": "Company Traded To",
        "REC_credits_traded": "REC Credits Traded",
        "is_offer_in_market": "Is Offer in Market",
        "price_of_contract": "Price of Contract",
    },
    inplace=True,
)

df.index = df.index + 1

# Display the DataFrame as a table
st.header("Completed Orders")
st.table(df)


# Generate a fake price vs. time chart for Amazon credits
col1, col2 = st.columns([2, 1], gap="medium")
