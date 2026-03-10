import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyCv6w3UL4vyDC0bZpL6xwZY11KwOAsL3VM")

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Search Medicine", layout="wide")

st.markdown("## Search Medicine")

medicine = st.text_input("Type medicine name...")

if medicine:

    prompt = f"""
    Explain the medicine {medicine} in simple language for elderly people.

    Provide sections:

    What is this medicine?
    How to take it
    Dosage
    Side Effects
    Precautions
    If You Miss a Dose
    Adverse Reaction — What to Do
    Medical Terms Explained
    """

    response = model.generate_content(prompt)

    result = response.text

    st.markdown("### Medicine Information")

    st.write(result)

    if st.button("🔊 Read Aloud"):
        st.write("Text to speech will be added here.")