import time
import streamlit as st
import pandas as pd
from navigation import make_sidebar

# Initialize Sidebar
make_sidebar()

# Custom CSS for styling
st.markdown(
    """
    <style>
    .select-companies-label {
        font-size: 24px;
        font-weight: bold;
    }
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

# Initialize MongoDB collections
db = st.session_state.dbClient["hackharvard"]
company_collection = db["company"]
rec_collection = db["business_rec"]

# Page Title
st.title("Energy Contract Marketplace")

# Filters Section
st.write("### Filters: ")
col1, col2 = st.columns(2)

# Slider for minimum amount of REC credits
with col1:
    min_amount = st.slider("Minimum Amount (metric tonnes)", 0.0, 500.0, 0.0, step=10.0)

# Slider for maximum price of contracts
with col2:
    max_price = st.slider("Maximum Price ($)", 0.0, 100000.0, 100000.0, step=500.0)

# Fetch available contracts from the database
contracts = (
    rec_collection.find(
        {
            "traded_from": {"$ne": st.session_state.username},
            "is_offer_in_market": True,
        }
    )
    .sort([("timestamp", -1)])
    .limit(10)
)
contracts = list(contracts)

# Apply filters to the contracts
available_credits = [
    credit
    for credit in contracts
    if credit["REC_credits_traded"] >= min_amount
    and credit["price_of_contract"] <= max_price
]

# Display Available Contracts
st.write("### Available Contracts: ")
selected_contracts = []

if available_credits:
    col1, col2 = st.columns([1, 1])

    # Display available contracts in a table
    with col1:
        df_available = pd.DataFrame(available_credits)
        df_available = df_available.drop(
            ["traded_to", "is_offer_in_market", "_id", "timestamp"],
            axis=1,
        )
        df_available = df_available.rename(
            columns={
                "traded_from": "Seller",
                "REC_credits_traded": "REC Credits",
                "price_of_contract": "Price of Contract",
                "datetime": "Date & Time",
            }
        )
        df_available.index = df_available.index + 1
        st.dataframe(df_available)

    # Checkbox for selecting contracts
    with col2:
        st.write("")
        st.write("")
        for cred in available_credits:
            is_selected = st.checkbox("", key=cred)
            selected_contracts.append((cred, is_selected))

    # Submit Button
    _, submit_col, _ = st.columns([1.5, 1, 1.5])
    with submit_col:
        if st.button("Purchase Certificate"):
            selected_credit = selected_contracts[0][0]
            total_cost = selected_credit["price_of_contract"]

            # Fetch company details
            company = list(
                company_collection.find({"name": st.session_state["username"]})
            )[0]

            # Update the purchased certificate in the database
            rec_collection.update_one(
                {"_id": selected_credit["_id"]},
                {
                    "$set": {
                        "traded_to": st.session_state.get("username", ""),
                        "is_offer_in_market": False,
                    }
                },
            )

            # Update company's balance and carbon balance
            company_collection.update_one(
                {"name": st.session_state["username"]},
                {
                    "$set": {
                        "money": company["money"] - total_cost,
                        "carbon_balance": company["carbon_balance"]
                        + selected_credit["REC_credits_traded"],
                    }
                },
            )

            # Success message and rerun
            st.success("Certificate Purchased Successfully.", icon="🚀")
            time.sleep(2)
            st.rerun()
else:
    st.info("No available contracts.")
