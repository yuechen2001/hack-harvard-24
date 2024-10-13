import streamlit as st
from navigation import make_sidebar
import pandas as pd


# Pull data from the collection.
def get_data():
    db = st.session_state.dbClient["hackharvard"]
    items = (
        db.household_rec.find({"user": st.session_state.username + "@gmail.com"})
        .sort([("timestamp", -1)])
        .limit(10)
    )
    items = list(items)
    print(items)

    for i in items:
        i['company_credits_earned'] = "{:.2f}".format(i['company_credits_earned'] * i['REC_credits_traded'])
        i['REC_credits_traded'] = "{:.0f}".format(i['REC_credits_traded'])

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
        "datetime": "Date & Time",
        "traded_to": "Company Traded To",
        "company_credits_earned": "Company Credits Earned",
        "REC_credits_traded": "REC Credits Traded In",
    },
    inplace=True,
)

df.index = df.index + 1

# Display the DataFrame as a table
st.write("### Completed Transactions:")
st.table(df)
