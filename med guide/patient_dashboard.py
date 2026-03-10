import streamlit as st
import datetime
from translations import get_text
from audio_helper import speak_text
# --- HERE IS THE CRUCIAL IMPORT YOU MENTIONED! ---
from ai_assistant import render_smart_assistant, translate_with_gemini, process_voice_message
from sms_helper import send_emergency_sms

def patient_view(username):
    p_data = st.session_state.patients[username]
    lang = st.session_state.language 
    
    # --- BUG FIXES & STATE TRACKING ---
    if 'alerted' not in p_data:
        p_data['alerted'] = {'Morning': False, 'Afternoon': False, 'Night': False}
    if 'profile_completed' not in p_data:
        p_data['profile_completed'] = False
    if 'sos_triggered' not in st.session_state:
        st.session_state.sos_triggered = False

    # --- SPEECH QUEUE HANDLER ---
    if 'speech_queue' not in st.session_state:
        st.session_state.speech_queue = ""
    if st.session_state.speech_queue:
        speak_text(st.session_state.speech_queue, lang)
        st.session_state.speech_queue = "" 
        
    # ==========================================
    # 🆕 THE ONBOARDING FORM
    # ==========================================
    if not p_data['profile_completed']:
        st.title("👋 Welcome to MedGuide!")
        st.subheader("Let's set up your medical profile first.")
        
        with st.form("onboarding_form"):
            name = st.text_input("Full Name", value=p_data.get('name', ''))
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
            address = st.text_area("Home Address (Crucial for Ambulance/SOS routing)")
            disease = st.text_input("Any Chronic Diseases? (e.g., Diabetes, Hypertension)")
            em_contact = st.text_input("Emergency Contact Number")
            
            submitted = st.form_submit_button("Save & Go to Dashboard", type="primary")
            
            if submitted:
                if not name or not address or not em_contact:
                    st.error("Please fill in your Name, Address, and Emergency Contact.")
                else:
                    p_data['name'] = name
                    p_data['age'] = age
                    p_data['address'] = address
                    p_data['chronic_disease'] = disease
                    p_data['emergency_contact'] = em_contact
                    p_data['profile_completed'] = True
                    st.session_state.speech_queue = "Profile saved successfully."
                    st.rerun()
        return
    # ==========================================

    sos_text = get_text(lang, 'sos_alert')
    if sos_text == 'sos_alert': 
        sos_text = "🚨 SOS Activated! Ambulance, family, and doctor are being contacted immediately."

    # --- EMERGENCY SOS BUTTON ---
    if st.button(get_text(lang, 'sos_btn'), type="primary", use_container_width=True):
        st.session_state.speech_queue = sos_text
        st.session_state.sos_triggered = True
        st.rerun()
    
    st.divider()

    # --- DYNAMIC TOAST & SMS ALERT LOGIC ---
    if st.session_state.sos_triggered:
        st.toast("🚨 EMERGENCY ALERT TRIGGERED! Contacting family & doctor...", icon="🚨")
        st.error(sos_text)
        
        doc_id = p_data.get('doctor')
        doc_name = st.session_state.doctors[doc_id]['name'] if doc_id and doc_id in st.session_state.doctors else None
        
        send_emergency_sms(
            emergency_contact=p_data['emergency_contact'],
            doctor_name=doc_name,
            patient_name=p_data['name'],
            address=p_data['address'],
            disease=p_data['chronic_disease']
        )
        
        st.session_state.sos_triggered = False
    else:
        st.toast(f"{get_text(lang, 'reminder')} {p_data['next_pill']}", icon="🔔")

    st.title(f"{p_data['name']}'s {get_text(lang, 'patient_dash').replace('My ', '')}")
    
    # --- TIME-BASED MISSED PILL LOGIC ---
    current_hour = datetime.datetime.now().hour
    missed_time_alerts = []
    
    if current_hour >= 12 and not p_data['meds']['Morning']:
        missed_time_alerts.append(get_text(lang, 'missed_morning_voice'))
    if current_hour >= 17 and not p_data['meds']['Afternoon']:
        missed_time_alerts.append(get_text(lang, 'missed_afternoon_voice'))
    if current_hour >= 23 and not p_data['meds']['Night']:
        missed_time_alerts.append(get_text(lang, 'missed_night_voice'))

    for alert in missed_time_alerts:
        st.warning(alert)
    
    read_aloud_label = f"🔊 {get_text(lang, 'patient_dash')} ({get_text(lang, 'read_aloud')})"
    if st.button(read_aloud_label):
        full_speech = f"{get_text(lang, 'reminder')} {p_data['next_pill']}. " + " ".join(missed_time_alerts)
        st.session_state.speech_queue = full_speech
        st.rerun()
    
    if not p_data['doctor']:
        st.warning(get_text(lang, 'no_doc_warn'))
        doc_id = st.text_input(get_text(lang, 'enter_doc_id'))
        if st.button(get_text(lang, 'link_doc_btn')):
            p_data['doctor'] = doc_id
            st.session_state.speech_queue = get_text(lang, 'doc_linked_speech')
            st.rerun()
            
    st.divider()
    
    # --- UNIFIED TAB LAYOUT ---
    tab_tracker, tab_ai, tab_chat = st.tabs(["💊 Medication Tracker", "🤖 Smart Assistant & Scanner", "💬 Doctor Chat"])
    
    with tab_tracker:
        st.subheader(get_text(lang, 'med_checklist'))
        cols = st.columns(3)
        time_keys = ['Morning', 'Afternoon', 'Night']
        ui_labels = [get_text(lang, 'morning'), get_text(lang, 'afternoon'), get_text(lang, 'night')]
        
        for i, time in enumerate(time_keys):
            with cols[i]:
                checked = st.checkbox(ui_labels[i], value=p_data['meds'][time], key=f"chk_{time}")
                if checked != p_data['meds'][time]:
                    p_data['meds'][time] = checked
                    if checked:
                        st.session_state.speech_queue = f"{ui_labels[i]} {get_text(lang, 'taken').replace('✅', '')}"
                    else:
                        st.session_state.speech_queue = f"{ui_labels[i]} {get_text(lang, 'unmarked_speech')}"
                        p_data['missed_count'] += 1
                    st.rerun()
                    
        if p_data['missed_count'] > 2:
            st.error(get_text(lang, 'emergency'))
            
        st.divider()
        
    with tab_ai:
        render_smart_assistant(username)
        
    with tab_chat:
        st.subheader(get_text(lang, 'live_chat'))
        chat_container = st.container(height=300)
        
        with chat_container:
            for i, msg in enumerate(p_data['chats']):
                with st.chat_message("user" if msg['sender'] == "Patient" else "assistant"):
                    display_text = msg['text']
                    
                    # --- AI REAL-TIME TRANSLATION ---
                    if msg['sender'] == 'Doctor' and lang != 'English':
                        if 'translations' not in msg:
                            msg['translations'] = {}
                            
                        if lang not in msg['translations']:
                            with st.spinner(f"Translating to {lang}..."):
                                msg['translations'][lang] = translate_with_gemini(msg['text'], lang)
                                
                        display_text = msg['translations'][lang]
                    
                    st.write(display_text)
                    
                    # --- READ ALOUD BUTTON FOR DOCTOR'S REPLY ---
                    if msg['sender'] == 'Doctor':
                        if st.button("🔊 Play Message", key=f"play_doc_{i}", size="small"):
                            st.session_state.speech_queue = display_text
                            st.rerun()
                            
                    st.caption(f"Status: {msg['status']}")
                    
        # --- OMNI-INPUT (TEXT + VOICE) ---
        new_msg = st.chat_input(get_text(lang, 'ask_doc'))
        audio_val = st.audio_input("🎙️ Record Voice Message (Auto-translates to English for Doctor)")
        
        if new_msg:
            p_data['chats'].append({'sender': 'Patient', 'text': new_msg, 'status': 'Under Process'})
            st.session_state.speech_queue = get_text(lang, 'msg_sent_speech')
            st.rerun()
            
        if audio_val:
            audio_hash = hash(audio_val.getvalue())
            if 'last_audio_hash' not in st.session_state or st.session_state.last_audio_hash != audio_hash:
                with st.spinner("Translating your voice to English for the doctor..."):
                    english_text = process_voice_message(audio_val.getvalue())
                    p_data['chats'].append({'sender': 'Patient', 'text': f"🎤 (Voice Note): {english_text}", 'status': 'Under Process'})
                    st.session_state.last_audio_hash = audio_hash
                    st.session_state.speech_queue = get_text(lang, 'msg_sent_speech')
                    st.rerun()