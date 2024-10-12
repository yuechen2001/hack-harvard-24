from datetime import datetime
import streamlit as st
import time

from navigation import make_sidebar

st.header("Update Consumer REC Credit Price")

st.markdown('<div class="stColumn">', unsafe_allow_html=True)

make_sidebar()

st.markdown(
    """
    <style>
    .select-companies-label {
        font-size: 24px;
        font-weight: bold;
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

# Display the label with the custom class
st.markdown(
    '<div class="select-companies-label">Update Consumer Credit Price: </div>',
    unsafe_allow_html=True,
)

with st.form("list_credits_form"):
    price = st.number_input("Price per Credit ($)", min_value=0, step=1)
    update = st.form_submit_button("Update")

    if update:
        collection = st.session_state.dbClient["hackharvard"]["company"]
        print(st.session_state.username)

        # Update the document
        result = collection.update_one(
            {"name": st.session_state.username},  # Filter to find the correct document
            {
                "$set": {"price_per_REC_credit": price}
            },  # Use $set to update the price field
        )

        if result.modified_count > 0:
            st.success("Price updated successfully!")
        else:
            st.warning("No document found with the specified company.")
