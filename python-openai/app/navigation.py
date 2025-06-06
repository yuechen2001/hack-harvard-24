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
                width: 100%;
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
        st.title("TradeREC")

        st.write("")
        st.write("")

        if st.session_state.get("is_logged_in", False):
            if st.session_state["role"] == "business":
                st.page_link(
                    "pages/business_dash.py", label="Company Dashboard", icon="🏠"
                )
                st.page_link("pages/business_market.py", label="Marketplace", icon="🛒")
                st.page_link(
                    "pages/business_list_credits.py",
                    label="Sell Clean Energy Contract (CEC)",
                    icon="⚡",
                )
                st.page_link(
                    "pages/business_household_price.py",
                    label="Set Credits to Spend per Household CEC credit",
                    icon="👤",
                )
            else:
                st.page_link(
                    "pages/household_upload_credits.py",
                    label="Sell Clean Energy Contract (CEC)",
                    icon="📤",
                )
                st.page_link(
                    "pages/household_transaction_history.py",
                    label="Transaction History",
                    icon="🕵️",
                )

            st.write("")
            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()


def logout():
    st.session_state.is_logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")
