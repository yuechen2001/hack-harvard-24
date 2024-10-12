import pymongo
import streamlit as st
from APIKeys import MONGO_URI
from navigation import make_sidebar

# Set page configuration
st.set_page_config(
    page_title="Role-Based Navigation", layout="wide", initial_sidebar_state="collapsed"
)
st.session_state["is_logged_in"] = False

# Define consumer credentials
users = {
    "business": {"password": "business123", "role": "business"},
    "consumer": {"password": "consumer123", "role": "consumer"},
}


# Function to handle login
def login(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state["is_logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        return True
    return False


make_sidebar()
username = st.text_input("Username")
password = st.text_input("Password", type="password")


def init_connection():
    return pymongo.MongoClient(MONGO_URI)


st.session_state.dbClient = init_connection()

# Check if the consumer is logged in, otherwise show login form
if st.button("Log in", type="primary"):
    if not st.session_state["is_logged_in"]:
        if login(username, password):
            st.success(f"Welcome, {username}")
            if st.session_state["role"] == "business":
                st.switch_page("pages/business_sell.py")
            else:
                st.switch_page("pages/consumer_upload_credits.py")
        else:
            st.error("Invalid username or password")
