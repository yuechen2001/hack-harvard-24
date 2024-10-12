import streamlit as st
from time import sleep


def make_sidebar():
    with st.sidebar:
        st.title("App Name Placeholder")
        st.write("")
        st.write("")

        if st.session_state.get("is_logged_in", False):
            if st.session_state["role"] == "business":
                st.page_link(
                    "pages/business_sell.py", label="Sell your Credits", icon="🔒"
                )
            else:
                st.page_link(
                    "pages/consumer_sell.py", label="Contract Management Dashboard", icon="🕵️"
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
