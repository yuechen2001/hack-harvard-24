import streamlit as st
import pymongo
from time import sleep

from APIKeys import MONGO_URI

# Set page configuration
st.set_page_config(
    page_title="Role-Based Navigation", layout="wide", initial_sidebar_state="collapsed"
)
st.session_state["is_logged_in"] = False

# Define household credentials
users = {
    "business": {"password": "business123", "role": "business"},
    "household": {"password": "household123", "role": "household"},
}

# Custom CSS for centralized form and narrower widgets
st.markdown(
    """
    <style>
        /* Style the input fields */
        input {
            width: 100%;  /* Full width of the container */
            padding: 10px;
            margin: 10px 0 20px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }

        /* Toast styling */
        .stToast {  
            background-color: #4CAF50; 
            color: white;
            padding: 20px;
            border-radius: 5px;
            font-size: 20px;
            text-align: center;
            width: 100%;
            max-width: 600px;
            margin: auto;
        }

        /* Error message styling */
        .stAlert {
            background-color: #ffcccb;
            color: red;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin: 20px 0;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# Function to handle login
def login(username):
    st.session_state["is_logged_in"] = True
    st.session_state["username"] = username
    if username == "eshan":
        st.session_state["role"] = "household"
    else:
        st.session_state["role"] = "business"
    return True


left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image("finance.png", width=640)

buff, login_col, buff2 = st.columns(3)
with login_col:
    st.write("### Please log in to continue.")

    # Username and password input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Log in button
    if st.button("Log in", type="primary"):
        if not st.session_state["is_logged_in"]:
            if login(username):
                st.toast(f"Welcome, {username}")
                sleep(1)
                if st.session_state["role"] == "business":
                    st.switch_page("pages/business_dash.py")
                else:
                    st.switch_page("pages/household_upload_credits.py")
            else:
                st.error("Invalid username or password")


# Initialize MongoDB connection
def init_connection():
    return pymongo.MongoClient(MONGO_URI)


st.session_state.dbClient = init_connection()
