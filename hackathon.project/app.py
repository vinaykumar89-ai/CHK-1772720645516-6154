import streamlit as st
from gtts import gTTS
import tempfile
import datetime
import json
import os

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("MedGuide Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):

            with open("users.json", "r") as f:
                users = json.load(f)

            found = False

            for user in users:
                if user["email"] == email and user["password"] == password:
                    found = True
                    break

            if found:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid login")

    with col2:
        if st.button("Create Account"):
            with open("users.json", "r") as f:
                users = json.load(f)

            users.append({"email": email, "password": password})

            with open("users.json", "w") as f:
                json.dump(users, f)

            st.success("Account created successfully")

    st.stop()

users_file = "users.json"

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return []

def save_user(email, password):
    users = load_users()
    users.append({"email": email, "password": password})
    with open(users_file, "w") as f:
        json.dump(users, f)

def authenticate(email, password):
    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == password:
            return True
    return False

if "page" not in st.session_state:
    st.session_state.page = "home"

st.set_page_config(page_title="MedGuide", layout="wide")

# -------- Text to Speech Function --------
def speak(text):
    tts = gTTS(text)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    return temp.name


# CSS
st.markdown("""
<style>

.main-title {
    text-align:center;
    background-color:#2f9e8f;
    padding:30px;
    border-radius:20px;
    color:white;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:white;
    font-size:18px;
}

.card{
    background-color:white;
    padding:30px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
    transition:0.3s;
}

.card:hover{
    transform:scale(1.05);
}

.green{
    background-color:#2f9e8f;
    color:white;
}

.orange{
    background-color:#f59f00;
    color:white;
}

.darkgreen{
    background-color:#2b8a3e;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-title">
 MedGuide
<div class="subtitle">Your simple medicine information helper</div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

st.markdown("<h2 style='text-align:center;'>What would you like to do?</h2>", unsafe_allow_html=True)

st.write("")

# Grid layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card green">
    <img src="https://cdn-icons-png.flaticon.com/512/751/751463.png" width="50">
    <h2>Search Medicine</h2>
    <p>Find by name</p>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="card orange">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSeobxuQMyRRj9SbjEGtazly8WakEH2USLAQ&s" width="60">
    <h2>Scan Barcode</h2>
    <p>Scan medicine QR / barcode</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card darkgreen">
    <img src="https://cdn-icons-png.flaticon.com/512/1827/1827392.png" width="60">
    <h2>Reminders</h2>
    <p>Set medicine alerts</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card orange">
    <img src="https://cdn-icons-png.flaticon.com/512/2961/2961948.png" width="60">
    <h2>History</h2>
    <p>Past searches</p>
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.write("---")



# can insert the code to create for the separate section like medical emergency and voice commands



st.write("")

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="card green">
    <img src="https://cdn-icons-png.flaticon.com/512/727/727269.png" width="60">
    <h2>Text to Speech</h2>
    <p>Listen to medicine instructions</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="card orange">
    <img src="https://cdn-icons-png.flaticon.com/512/2966/2966327.png" width="60">
    <h2>Medical Alert</h2>
    <p>Emergency help button</p>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:

    st.title("MedGuide Login")

    option = st.radio("Select", ["Login", "Create Account"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if authenticate(email, password):
                st.session_state.logged_in = True
                st.success("Login successful")
            else:
                st.error("Invalid email or password")

    else:
        if st.button("Create Account"):
            save_user(email, password)
            st.success("Account created. Please login.")

    st.stop()




