import streamlit as st
from navigation import make_sidebar
import pandas as pd

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

st.title("Contract Management Dashboard")

# Completed orders data
data = {
    "Date Completed": ["October 9, 2024", "October 8, 2024", "October 7, 2024"],
    "Traded to": ["Apple", "Amazon", "Walmart"],
    "Company Credits Earned": ["$200", "$500", "$345"],
    "RECs Traded": [150, 200, 100],
    "Company Credits Earned": ["$200", "$500", "$345"],
}

# Create a DataFrame
df = pd.DataFrame(data, columns=data.keys(), index=[1, 2, 3])

# Display the DataFrame as a table
st.header("Completed Orders")
st.table(df)
