import streamlit as st
import pandas as pd
from navigation import make_sidebar

# Initialize session state for balances, credits, and purchases
if "credits" not in st.session_state:
    st.session_state["credits"] = []

if "purchased_credits" not in st.session_state:
    st.session_state["purchased_credits"] = []

if "balance" not in st.session_state and st.session_state.get("role") == "business":
    st.session_state["balance"] = 100000  # Initial balance for businesses

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


# Function to display the business dashboard
def business_dashboard():
    st.header("Business Dashboard")

    # Display Current Balance
    st.subheader("Current Balance")
    st.write(f"**${st.session_state['balance']:.2f}**")

    # Display Purchased Credits
    st.subheader("Purchased Carbon Credits")
    if st.session_state["purchased_credits"]:
        df_purchased = pd.DataFrame(st.session_state["purchased_credits"])
        st.table(df_purchased)

        # Calculate Total Value
        total_value = df_purchased["Price"].sum()
        st.write(f"**Total Value of Purchased Credits:** ${total_value:.2f}")

        # Calculate Total Carbon Emission Offset
        total_offset = df_purchased["Amount"].sum()
        st.write(
            f"**Total Carbon Emission Offset:** {total_offset} metric tonnes of CO₂"
        )
    else:
        st.info("No credits purchased yet.")


# Function to browse and purchase credits (for businesses)
def browse_and_purchase():
    st.header("Browse Carbon Credits")

    # Centered Filters using Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        min_amount = st.slider(
            "Minimum Amount (metric tonnes)", 0.0, 500.0, 0.0, step=10.0
        )

    with col2:
        max_price = st.slider("Maximum Price ($)", 0.0, 1000.0, 1000.0, step=50.0)

    with col3:
        verified_only = st.checkbox("Show Only Verified Credits")

    # Apply Filters
    available_credits = [
        credit
        for credit in st.session_state["credits"]
        if credit["Purchased By"] is None
        and credit["Amount"] >= min_amount
        and credit["Price"] <= max_price
        and (credit["Verified"] if verified_only else True)
    ]

    if available_credits:
        df_available = pd.DataFrame(available_credits)
        st.dataframe(df_available)

        credit_index = st.number_input(
            "Select Credit ID to Purchase",
            min_value=0,
            max_value=len(available_credits) - 1,
            step=1,
            format="%d",
        )

        if st.button("Purchase Selected Credit"):
            selected_credit = available_credits[int(credit_index)]
            total_cost = selected_credit["Amount"] * selected_credit["Price"]

            if total_cost > st.session_state["balance"]:
                st.error("Insufficient balance to complete the purchase.")
            else:
                # Deduct Balance and Update Credit Ownership
                index = next(
                    i
                    for i, credit in enumerate(st.session_state["credits"])
                    if credit == selected_credit
                )
                selected_credit["Purchased By"] = st.session_state.get("username", "")
                st.session_state["purchased_credits"].append(selected_credit)
                del available_credits[int(credit_index)]
                df_available.drop(index=index, inplace=True)
                # Update balance after purchase
                st.session_state["balance"] -= total_cost
                print(
                    st.session_state["credits"]
                )  # Debugging: Verify update in credits list
                print(
                    st.session_state["purchased_credits"]
                )  # Debugging: Verify purchased credits list
                print(st.session_state["balance"])  # Debugging: Verify balance update
                st.success(
                    f"Purchased {selected_credit['Amount']} metric tonnes of CO₂ credits for ${total_cost:.2f}"
                )
                # Refresh the page to show updated data
                st.rerun()
    else:
        st.info("No available credits match your filters.")


# Main Function to Handle Role-Based Navigation
def main():
    business_dashboard()
    browse_and_purchase()


if __name__ == "__main__":
    main()
