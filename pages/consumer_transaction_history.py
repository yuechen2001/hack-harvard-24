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


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = st.session_state.dbClient["hackharvard"]
    items = (
        db.consumer_rec.find({"user": "consumer@gmail.com"})
        .sort([("timestamp", -1)])
        .limit(10)
    )
    items = list(items)  # make hashable for st.cache_data
    return items


make_sidebar()

st.title("Transaction History")

# Completed orders data
data = get_data()

# Remove '_id' field from each document
for document in data:
    document.pop("_id", None)
    document.pop("user", None)
    document.pop("timestamp", None)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(
    data,
)

df.rename(
    columns={
        "datetime": "Date",
        "traded_to": "Company Traded To",
        "company_credits_earned": "Company Credits Earned",
        "REC_credits_traded": "REC Credits Traded In",
    },
    inplace=True,
)

df.index = df.index + 1

# Display the DataFrame as a table
st.header("Completed Orders")
st.table(df)
