import streamlit as st
import json
from openai import OpenAI
from APIKeys import OPEN_AI_API_KEY
from navigation import make_sidebar


client = OpenAI(api_key=OPEN_AI_API_KEY)

st.markdown(
    """
    <style>
        .stColumn {
            # border: 2px solid #f0f0f0;
            padding: 20px;
            border-radius: 5px;
        }
        .stTextInput input, .stButton button {
            width: 100%;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .stButton button {
            background-color: #28a745;
            color: white;
        }
        .stButton button:hover {
            background-color: #218838;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

make_sidebar()


def parse_rec(rec):
    try:
        prompt = (
            "I am passing in the text from a Renewable Energy Certificate (REC). Parse the text and output in the JSON format below:\n"
            '{"certifier": "the name of the company/organization that certified this REC", "user": "the name of the organization/user the REC was awarded to", "co2": "the number of metric tonnes of CO2 that was offset"}.\n'
            "Here is the text from the REC:\\" + rec + "\n"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.4,
        )
        if response.choices[0].message.content is not None:
            return json.loads(response.choices[0].message.content)
        return ""
    except Exception as e:
        return f"Error: {e}"


if "file_processed" not in st.session_state:
    st.session_state["file_processed"] = False
if "parsed_rec" not in st.session_state:
    st.session_state["parsed_rec"] = None

st.title("Contract Management Dashboard")

# Create two columns: Active Contracts and Completed Orders
col1, col2 = st.columns(2)

# Left column: Active Contracts
with col1:
    st.header("Active Contracts")

    # Example of an active contract
    st.subheader("Date: October 10, 2024")
    st.text("Tons of CO2: 100")
    st.text("Companies: Amazon, Walmart, Apple")

    # Add more contracts as needed
    st.subheader("Date: October 11, 2024")
    st.text("Tons of CO2: 250")
    st.text("Companies: Netflix, Airbnb")

    st.subheader("Date: October 12, 2024")
    st.text("Tons of CO2: 300")
    st.text("Companies: Nike, Samsung")

# Right column: Completed Orders
with col2:
    st.header("Completed Orders")

    # Example of a completed order
    st.subheader("Date Completed: October 9, 2024")
    st.text("Tons of CO2: 150")
    st.text("Money Earned: $10,000")
    st.text("Fulfilled by: Apple")

    # Add more completed orders as needed
    st.subheader("Date Completed: October 8, 2024")
    st.text("Tons of CO2: 200")
    st.text("Money Earned: $15,000")
    st.text("Fulfilled by: Amazon")

    st.subheader("Date Completed: October 7, 2024")
    st.text("Tons of CO2: 100")
    st.text("Money Earned: $5,000")
    st.text("Fulfilled by: Walmart")
