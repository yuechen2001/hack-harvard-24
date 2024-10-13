import streamlit as st
import pandas as pd
from navigation import make_sidebar

# Initialize Sidebar
make_sidebar()

# Set Page Title
st.title("Company Dashboard")


# Function to get transaction data
def get_transaction_data():
    db = st.session_state.dbClient["hackharvard"]
    items = (
        db.business_rec.find(
            {
                "traded_from": st.session_state.username + "@gmail.com",
                "is_offer_in_market": False,
            }
        )
        .sort([("timestamp", -1)])
        .limit(10)
    )
    return list(items)


# Function to get business data
def get_business_data():
    db = st.session_state.dbClient["hackharvard"]
    return db.company.find_one({"name": st.session_state.username})


# Custom CSS
st.markdown(
    """
    <style>
        .stColumn {
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

# Set default market price if not already set
if "market_price" not in st.session_state:
    st.session_state["market_price"] = 100  # Placeholder for actual market price

# Get business data
business = get_business_data()
company_name = business["name"]
company_logo_url = business["image_url"]

# Create two columns for the company logo and business details
col1, col2 = st.columns(2)

# Display company logo in the first column
with col1:
    st.markdown(
        f"""
        <div class="logo-container">
            <img class="logo-image" src="{company_logo_url}" alt="{company_name} Logo" width="400">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display carbon balance and wallet balance in the second column
with col2:
    st.markdown(
        f"""
        <div class="grey-box">
            <h2>Carbon Balance: </h2>
            <h3> {business['carbon_balance']} metric tonnes of CO2</h3>
            <h2>Wallet Balance: </h2>
            <h3> $ {business['money']:.2f}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Fetch and clean transaction data
data = get_transaction_data()

# Remove unwanted fields from each document
for document in data:
    document.pop("_id", None)
    document.pop("traded_from", None)
    document.pop("timestamp", None)
    document.pop("is_offer_in_market", None)

# Convert transaction data to DataFrame
df = pd.DataFrame(data)

# Rename columns for better readability
df.rename(
    columns={
        "datetime": "Date & Time",
        "traded_to": "Company Traded To",
        "REC_credits_traded": "CEC Credits Obtained",
        "price_of_contract": "Total Value of Contract (USD)",
    },
    inplace=True,
)

# Adjust index to start from 1
df.index = df.index + 1

# Display completed sales
st.write("### Completed Sales:")
st.table(df)

# Generate placeholder columns for future use
col1, col2 = st.columns([2, 1], gap="medium")
