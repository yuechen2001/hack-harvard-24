import streamlit as st
import pandas as pd
from navigation import make_sidebar

make_sidebar()

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
    </style>
    """,
    unsafe_allow_html=True,
)

db = st.session_state.dbClient["hackharvard"]
company_collection = db["company"]
rec_collection = db["business_rec"]

st.header("Energy Contract Marketplace")
# Centered Filters using Columns
col1, col2 = st.columns(2)

with col1:
    min_amount = st.slider("Minimum Amount (metric tonnes)", 0.0, 500.0, 0.0, step=10.0)

with col2:
    max_price = st.slider("Maximum Price ($)", 0.0, 1000.0, 1000.0, step=50.0)

db = st.session_state.dbClient["hackharvard"]
contracts = (
    rec_collection.find(
        {"traded_from": {"$ne": st.session_state.username + "@gmail.com"}}
    )
    .sort([("timestamp", -1)])
    .limit(10)
)
contracts = list(contracts)
print(contracts)

# Apply Filters
available_credits = [
    credit
    for credit in contracts
    if credit["is_offer_in_market"]
    and credit["REC_credits_traded"] >= min_amount
    and credit["price_of_contract"] <= max_price
]

selected_contracts = []
if available_credits:
    col1, col2 = st.columns([5, 1])
    with col1:
        df_available = pd.DataFrame(available_credits)
        df_available = df_available.drop("_id", axis=1)
        st.dataframe(df_available)
    with col2:
        for cred in available_credits:
            is_selected = st.checkbox("", key=cred)
            selected_contracts.append((cred, is_selected))

    if st.button("Purchase Selected Credit"):
        selected_credit = selected_contracts[0][0]
        print(selected_credit)
        total_cost = (
            int(selected_credit["REC_credits_traded"])
            * selected_credit["price_of_contract"]
        )

        index = next(
            i for i, credit in enumerate(contracts) if credit == selected_credit
        )

        company = list(company_collection.find({"name": st.session_state["username"]}))[
            0
        ]

        rec_collection.update_one(
            {"_id": selected_credit["_id"]},
            {
                "$set": {
                    "traded_to": st.session_state.get("username", "") + "@gmail.com",
                    "is_offer_in_market": False,
                }
            },
        )
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
        st.rerun()
else:
    st.info("No available credits match your filters.")
