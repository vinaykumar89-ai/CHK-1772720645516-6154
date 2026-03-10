import streamlit as st
from gtts import gTTS
import tempfile

# Language selector
language = st.selectbox(
    "Choose Language / भाषा निवडा / भाषा चुनें",
    ["English", "Hindi", "Marathi"]
)

# Translation dictionary
translations = {

    "English": {
        "title": "Text to Speech",
        "input": "Enter medicine explanation",
        "button": "Generate Speech"
    },

    "Hindi": {
        "title": "टेक्स्ट को आवाज़ में बदलें",
        "input": "दवा की जानकारी लिखें",
        "button": "आवाज़ बनाएं"
    },

    "Marathi": {
        "title": "मजकूर आवाजात बदला",
        "input": "औषधाची माहिती लिहा",
        "button": "आवाज तयार करा"
    }
}

# Select language dictionary
t = translations[language]

st.title(t["title"])

text = st.text_area(t["input"])

if st.button(t["button"]):

    if text == "":
        st.warning("Please enter text")

    else:

        # Language code for speech
        lang_code = "en"

        if language == "Hindi":
            lang_code = "hi"

        elif language == "Marathi":
            lang_code = "mr"

        tts = gTTS(text=text, lang=lang_code)

        temp_file = tempfile.NamedTemporaryFile(delete=False)

        tts.save(temp_file.name)

        st.audio(temp_file.name)