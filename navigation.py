import streamlit as st
from time import sleep


def make_sidebar():
    # Add custom CSS
    st.markdown(
        """
        <style>
            /* Customize the sidebar title */
            .css-18e3th9 {
                font-size: 22px;
                font-weight: bold;
                color: #4CAF50; /* Green color */
            }

            /* Customize all buttons */
            .stButton>button {
                background-color: #4CAF50; /* Green background */
                color: white;
                border-radius: 8px;
                padding: 10px;
            }

            /* Hover effect for buttons */
            .stButton>button:hover {
                background-color: #45a049; /* Darker green */
            }

            /* Add padding between sidebar elements */
            .sidebar-content > *:not(:last-child) {
                margin-bottom: 20px;
            }
            
            /* Customize page links (streamlit-expander) */
            .streamlit-expanderHeader {
                font-size: 18px;
                font-weight: bold;
                color: #2C3E50;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("App Name Placeholder")
        st.write("")
        st.write("")

        if st.session_state.get("is_logged_in", False):
            if st.session_state["role"] == "business":
                st.page_link(
                    "pages/business_dash.py", label="Dashboard", icon="🏠"
                )
                st.page_link(
                    "pages/business_market.py", label="MarketPlace", icon="🛒"
                )
                st.page_link(
                    "pages/business_list_credits.py", label="List Energy Credits", icon="⚡"
                )
            else:
                st.page_link(
                    "pages/consumer_transaction_history.py",
                    label="Contract Management Dashboard",
                    icon="🕵️",
                )
                st.page_link(
                    "pages/consumer_upload_credits.py",
                    label="Upload Clean Energy Contract",
                    icon="📤",
                )

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()


def logout():
    st.session_state.is_logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")
