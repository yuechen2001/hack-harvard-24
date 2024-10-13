import streamlit as st
import pymongo
from time import sleep
from APIKeys import MONGO_URI

# Set page configuration
st.set_page_config(
    page_title="TradeREC - Login",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Set session state for login status
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

# Define users and their credentials
users = {
    "business": {"password": "business123", "role": "business"},
    "household": {"password": "household123", "role": "household"},
}

# Custom CSS for better form alignment and styling
st.markdown(
    """
    <style>
        /* Center the entire form container */
        .login-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: auto;
            text-align: center;
            padding: 1px;
            margin-top: -200px;  /* Further reduced margin at the top */
        }

        /* Style the input fields */
        input {
            width: 100%;
            padding: 8px;  /* Reduced padding */
            margin: 0px 0 0px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 14px;  /* Reduced font size */
            background-color: #f8f8f8;
        }

        /* Style the login button */
        .stButton > button {
            background-color: #ff4b4b !important;
            color: white !important;
            padding: 8px;
            width: 100%;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }

        .stButton > button:hover {
            background-color: #ff6b6b !important;
        }

        /* Form error message */
        .error-message {
            color: red;
            margin-top: 15px;
            font-size: 14px;
        }

        /* Center the image */
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 20px;  /* Reduced space below image */
            width: 35%;  /* Made the logo smaller */
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Function to handle login
def login(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state["is_logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        return True
    return False


# Main login form
with st.container():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Add logo image
    st.image("finance.png", use_column_width=True, caption="TradeREC")

    # Username and password fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Log in button
    if st.button("Log in"):
        if not st.session_state["is_logged_in"]:
            if login(username, password):
                st.success(f"Welcome, {username}")
                sleep(1)
                if st.session_state["role"] == "business":
                    st.experimental_rerun()  # Redirect to business dashboard page
                else:
                    st.experimental_rerun()  # Redirect to household upload page
            else:
                st.markdown(
                    '<p class="error-message">Invalid username or password</p>',
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


# Initialize MongoDB connection
def init_connection():
    return pymongo.MongoClient(MONGO_URI)


st.session_state.dbClient = init_connection()
