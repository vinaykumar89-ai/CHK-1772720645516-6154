import streamlit as st
from mock_database import init_db
from doctor_dashboard import doctor_view
from patient_dashboard import patient_view

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ElderCare Pro", layout="wide")

# --- ELDER-FRIENDLY CSS INJECTION ---
def apply_custom_css():
    st.markdown("""
        <style>
        /* Global Font and Text Size for Readability */
        html, body, [class*="st-"] {
            font-family: 'Segoe UI', Roboto, Helvetica, sans-serif !important;
            font-size: 20px !important; 
        }
        
        /* Bold, High-Contrast Headers */
        h1 { font-size: 2.5rem !important; color: #1E3A8A !important; font-weight: 800 !important; }
        h2 { font-size: 2rem !important; color: #2563EB !important; font-weight: 700 !important; }
        h3 { font-size: 1.75rem !important; color: #3B82F6 !important; font-weight: 600 !important; }

        /* Huge Buttons (Easy to tap on mobile/tablets) */
        .stButton > button {
            width: 100%;
            min-height: 70px;
            font-size: 24px !important;
            font-weight: bold;
            background-color: #2563EB !important;
            color: white !important;
            border-radius: 12px;
            border: 2px solid #1D4ED8;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1D4ED8 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }

        /* Extra Large Checkboxes for Medication Tracking */
        div[data-baseweb="checkbox"] > div {
            transform: scale(1.6);
            margin-right: 15px;
        }
        div[data-baseweb="checkbox"] label {
            font-size: 24px !important;
            font-weight: 500 !important;
            color: #111827 !important;
        }

        /* Clear, large input fields */
        .stTextInput input {
            font-size: 22px !important;
            padding: 15px !important;
            border-radius: 8px !important;
            border: 2px solid #9CA3AF !important;
        }
        
        /* High visibility alerts */
        .stAlert {
            border-radius: 12px !important;
            border-left: 8px solid !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the styles immediately
apply_custom_css()

# Initialize the mock database
init_db()

# --- INITIALIZE ALL SESSION STATES ---
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'language_selected' not in st.session_state:
    st.session_state.language_selected = False
if 'language' not in st.session_state:
    st.session_state.language = "English"

# --- SCREEN 1: LOGIN ---
if st.session_state.logged_in_user is None:
    st.title("🏥 ElderCare Portal Login")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Secure Sign In")
        role = st.selectbox("I am a:", ["Patient", "Doctor"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Log In"):
            if role == "Patient" and username in st.session_state.users and password == st.session_state.users[username]:
                st.session_state.logged_in_user = username
                st.session_state.user_role = "Patient"
                st.rerun()
            elif role == "Doctor" and username in st.session_state.users and password == st.session_state.users[username]:
                st.session_state.logged_in_user = username
                st.session_state.user_role = "Doctor"
                st.rerun()
            else:
                st.error("Invalid credentials. Please check your username and password.")
                
    with col2:
        st.info("**System Access Directory**\n\n**Patient Login:**\nUsername: `patient1`\nPassword: `1234`\n\n**Doctor Login:**\nUsername: `doctor1`\nPassword: `admin`")

# --- SCREEN 2: LANGUAGE SELECTION ---
elif not st.session_state.language_selected:
    st.title("🌐 Select Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ / भाषा चुनें / भाषा निवडा")
    
    chosen_lang = st.selectbox(
        "Language / ಭಾಷೆ / भाषा / भाषा", 
        ["English", "Kannada", "Hindi", "Marathi"]
    )
    
    if st.button("Continue / ಮುಂದುವರಿಸಿ / जारी रखें / पुढे जा"):
        st.session_state.language = chosen_lang
        st.session_state.language_selected = True
        st.rerun()

# --- SCREEN 3: MAIN DASHBOARDS ---
else:
    # Sidebar navigation
    st.sidebar.title(f"Role: {st.session_state.user_role}")
    st.sidebar.success(f"User ID: {st.session_state.logged_in_user}")
    st.sidebar.info(f"Language: {st.session_state.language}")
    
    if st.sidebar.button("🚪 Log Out"):
        # Reset all session states so the next user starts fresh
        st.session_state.logged_in_user = None
        st.session_state.user_role = None
        st.session_state.language_selected = False 
        st.rerun()
        
    # Route to correct dashboard
    if st.session_state.user_role == "Patient":
        patient_view(st.session_state.logged_in_user)
    else:
        doctor_view(st.session_state.logged_in_user)