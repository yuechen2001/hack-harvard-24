import streamlit as st
import pandas as pd
import numpy as np
from navigation import make_sidebar

make_sidebar()

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Company information (logo and hardcoded price)
company_name = "Amazon"
company_logo_url = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"  # Replace with your actual logo URL
credit_price = 123.45  # Hardcoded credit price

# Custom CSS to add a white background to the logo container and grey box for text
st.markdown(
    """
    <style>
    .logo-container {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
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
            <img src="{company_logo_url}" alt="{company_name} Logo" width="400">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display the credit price in the second column (on the right) wrapped in a grey box
with col2:
    st.markdown(
        f"""
        <div class="grey-box">
            <h2>Company name: {company_name}</h2>
            <h3>No. of {company_name} credits per Energy credit: <b>${credit_price}</b></h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Generate a fake price vs. time chart for Amazon credits
st.write("### Price of Amazon Credits Over Time")


# Create a fake dataset
dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
price_changes = (
    np.random.randn(100).cumsum() + credit_price
)  # Random walk around the credit price

# Create a dataframe
df = pd.DataFrame({"Date": dates, "Amazon Credit Price": price_changes})

# Plot the line chart
st.line_chart(df.set_index("Date"))
