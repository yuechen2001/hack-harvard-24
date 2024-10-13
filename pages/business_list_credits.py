from navigation import make_sidebar
from openai import OpenAI
import streamlit as st
import pytesseract
from PIL import Image
import json
import time

from APIKeys import OPEN_AI_API_KEY, MONGO_URI
from navigation import make_sidebar
from datetime import datetime

make_sidebar()

client = OpenAI(api_key=OPEN_AI_API_KEY)
st.session_state["file_processed"] = False
st.session_state["parsed_rec"] = {"co2": 0, "user": "test", "certifier": "test"}

db = st.session_state.dbClient["hackharvard"]
rec_collection = db["business_rec"]


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


st.title("List Your Clean Energy Contract (CEC)")

# Display the label with the custom class
st.write("### Upload your Renewable Energy Certificate (REC):")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Renewable Energy Certificate (REC)", use_column_width=True)

    if not st.session_state["file_processed"]:
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        extracted_text = pytesseract.image_to_string(image)
        parsed_rec = parse_rec(extracted_text)
        st.session_state["parsed_rec"] = parsed_rec
    else:
        parsed_rec = st.session_state["parsed_rec"]

    st.text("Certifier: " + parsed_rec["certifier"])
    st.text("Awardee: " + parsed_rec["user"])
    st.text("CO₂ Offset (metric tonnes): " + parsed_rec["co2"])

    if not st.session_state["file_processed"]:
        with st.spinner("Processing..."):
            time.sleep(2)

    if parsed_rec["co2"] == "250":
        st.success("REC Verified")
        st.session_state["file_processed"] = True
    else:
        st.error("REC Invalid")
        st.session_state["file_processed"] = False


col, _ = st.columns(2)
with col:
    if st.session_state["file_processed"]:
        with st.form("list_credits_form"):
            st.write("### Set Credit Price: ")
            price = st.number_input("Price per Credit ($)", min_value=0, step=1)
            submit = st.form_submit_button("List Credits")

            if submit:
                if int(st.session_state["parsed_rec"]["co2"]) > 0:
                    st.text(
                        str(st.session_state["parsed_rec"]["co2"])
                        + " x "
                        + str(price)
                        + " = $"
                        + str(int(st.session_state["parsed_rec"]["co2"]) * price)
                    )
                parsed_rec = st.session_state["parsed_rec"]
                contract = {
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "timestamp": time.time(),
                    "traded_to": "",
                    "REC_credits_traded": int(parsed_rec["co2"]),
                    "is_offer_in_market": True,
                    "price_of_contract": int(parsed_rec["co2"]) * price,
                    "traded_from": st.session_state["username"],
                }
                rec_collection.insert_one(contract)
                st.session_state["file_processed"] = False
                st.session_state["parsed_rec"] = {
                    "co2": 0,
                    "user": "test",
                    "certifier": "test",
                }
                st.success("CEC Listed Successfully.", icon="🚀")
