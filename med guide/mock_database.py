import streamlit as st

def init_db():
    if 'users' not in st.session_state:
        st.session_state.users = {'patient1': '1234', 'doctor1': 'admin'}
        
    if 'patients' not in st.session_state:
        st.session_state.patients = {
            'patient1': {
                'name': 'John Doe',
                'doctor': None,
                'missed_count': 0,
                'meds': {'Morning': False, 'Afternoon': False, 'Night': False},
                'chats': [],
                'next_pill': 'Afternoon (Metformin)'
            }
        }
        
    if 'doctors' not in st.session_state:
        st.session_state.doctors = {
            'doctor1': {
                'name': 'Dr. Sarah Smith', 
                'appointments': ['John Doe requested a checkup for this Friday at 10:00 AM.']
            }
        }