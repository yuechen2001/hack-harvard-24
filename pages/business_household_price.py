from datetime import datetime
import streamlit as st

from navigation import make_sidebar

st.title("Set Credits to Spend per Household CEC credit")

make_sidebar()

# Display the label with the custom class
st.write(f"### Set Credit Price: ")

col, _ = st.columns(2)

with col:
    with st.form("list_credits_form"):
        price = st.number_input("Price per Credit ($)", min_value=0, step=1)
        update = st.form_submit_button("Update")

        if update:
            collection = st.session_state.dbClient["hackharvard"]["company"]

            # Update the document
            result = collection.update_one(
                {
                    "name": st.session_state.username
                },  # Filter to find the correct document
                {
                    "$set": {"price_per_REC_credit": price}
                },  # Use $set to update the price field
            )

            if result.modified_count > 0:
                st.success("Credit Price Updated.")
            else:
                st.warning("No document found with the specified company.")
