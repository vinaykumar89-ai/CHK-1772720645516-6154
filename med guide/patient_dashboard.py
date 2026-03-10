import streamlit as st
from scanner import render_scanner
from translations import get_text
from audio_helper import speak_text

def patient_view(username):
    p_data = st.session_state.patients[username]
    lang = st.session_state.language 
    
    # --- SPEECH QUEUE HANDLER ---
    if 'speech_queue' not in st.session_state:
        st.session_state.speech_queue = ""
        
    if st.session_state.speech_queue:
        speak_text(st.session_state.speech_queue, lang)
        st.session_state.speech_queue = "" 
    # -----------------------------

    st.toast(f"{get_text(lang, 'reminder')} {p_data['next_pill']}", icon="🔔")
    
    st.title(get_text(lang, 'patient_dash'))
    
    # Fully translated Read Aloud button and speech payload
    read_aloud_label = f"🔊 {get_text(lang, 'patient_dash')} ({get_text(lang, 'read_aloud')})"
    if st.button(read_aloud_label):
        st.session_state.speech_queue = f"{get_text(lang, 'reminder')} {p_data['next_pill']}."
        st.rerun()
    
    if not p_data['doctor']:
        st.warning(get_text(lang, 'no_doc_warn'))
        doc_id = st.text_input(get_text(lang, 'enter_doc_id'))
        if st.button(get_text(lang, 'link_doc_btn')):
            p_data['doctor'] = doc_id
            st.session_state.speech_queue = get_text(lang, 'doc_linked_speech')
            st.rerun()
            
    st.divider()
    
    st.subheader(get_text(lang, 'med_checklist'))
    cols = st.columns(3)
    
    time_keys = ['Morning', 'Afternoon', 'Night']
    ui_labels = [get_text(lang, 'morning'), get_text(lang, 'afternoon'), get_text(lang, 'night')]
    
    for i, time in enumerate(time_keys):
        with cols[i]:
            checked = st.checkbox(ui_labels[i], value=p_data['meds'][time], key=f"chk_{time}")
            if checked != p_data['meds'][time]:
                p_data['meds'][time] = checked
                
                # Fetching the translated spoken feedback
                if checked:
                    # e.g., "सकाळचे औषध घेतले"
                    st.session_state.speech_queue = f"{ui_labels[i]} {get_text(lang, 'taken').replace('✅', '')}"
                else:
                    # e.g., "सकाळचे औषध काढून टाकले"
                    st.session_state.speech_queue = f"{ui_labels[i]} {get_text(lang, 'unmarked_speech')}"
                    p_data['missed_count'] += 1
                    
                st.rerun()
                
    if p_data['missed_count'] > 2:
        st.error(get_text(lang, 'emergency'))
        
    st.divider()
    render_scanner()
    st.divider()
    
    st.subheader(get_text(lang, 'live_chat'))
    chat_container = st.container(height=300)
    
    with chat_container:
        for msg in p_data['chats']:
            with st.chat_message("user" if msg['sender'] == "Patient" else "assistant"):
                st.write(msg['text'])
                st.caption(f"Status: {msg['status']}")
                
    new_msg = st.chat_input(get_text(lang, 'ask_doc'))
    if new_msg:
        p_data['chats'].append({'sender': 'Patient', 'text': new_msg, 'status': 'Under Process'})
        st.session_state.speech_queue = get_text(lang, 'msg_sent_speech')
        st.rerun()