import streamlit as st

def doctor_view(username):
    # Retrieve the doctor's database record
    d_data = st.session_state.doctors[username]
    lang = st.session_state.language
    
    st.title(f"🩺 {d_data['name']}'s Portal")
    
    # --- AUTOMATIC PATIENT LINKING ---
    # This automatically searches the database and grabs any patient who linked to this specific doctor
    my_patients = {p_id: p_info for p_id, p_info in st.session_state.patients.items() if p_info.get('doctor') == username}
    
    tab_overview, tab_queries = st.tabs(["👥 Patient Overview", "💬 Active Messages"])
    
    # ==========================================
    # TAB 1: PATIENT MONITORING
    # ==========================================
    with tab_overview:
        st.subheader("Linked Patients & Health Status")
        if not my_patients:
            st.info(f"No patients linked yet. Tell your patients to enter your username: **{username}** on their dashboard to connect.")
            
        for p_id, p in my_patients.items():
            # Create a dropdown card for each linked patient
            with st.expander(f"👤 {p.get('name', 'Unknown Patient')} | Missed Pills: {p['missed_count']}"):
                
                # Show the personal details they filled out in the onboarding form!
                st.write(f"**Age:** {p.get('age', 'N/A')} | **Conditions:** {p.get('chronic_disease', 'None')}")
                st.write(f"**Emergency Contact:** `{p.get('emergency_contact', 'N/A')}`")
                
                # Live Pill Tracker
                cols = st.columns(3)
                cols[0].metric("Morning", "Taken ✅" if p['meds']['Morning'] else "Pending ⏳")
                cols[1].metric("Afternoon", "Taken ✅" if p['meds']['Afternoon'] else "Pending ⏳")
                cols[2].metric("Night", "Taken ✅" if p['meds']['Night'] else "Pending ⏳")
                
                if p['missed_count'] > 2:
                    st.error("🚨 High Risk: Patient is missing medications frequently.")
    
    # ==========================================
    # TAB 2: LIVE CHAT MANAGEMENT
    # ==========================================
    with tab_queries:
        st.subheader("Patient Messages & Inquiries")
        
        if not my_patients:
            st.write("No patients linked.")
        else:
            has_active_queries = False
            
            # Loop through every patient belonging to this doctor
            for p_id, p in my_patients.items():
                
                # Check if this specific patient has any unanswered messages
                unresolved_chats = [c for c in p['chats'] if c.get('status') == 'Under Process']
                
                if unresolved_chats:
                    has_active_queries = True
                    st.markdown(f"### 📩 Message from {p.get('name', 'Unknown')}")
                    
                    for i, msg in enumerate(p['chats']):
                        if msg.get('status') == 'Under Process':
                            # Display the patient's question
                            st.info(f"**Question:** {msg['text']}")
                            
                            # Provide an input box for the doctor to type a reply
                            reply = st.text_input("Type your medical advice/reply here:", key=f"reply_{p_id}_{i}")
                            
                            cols = st.columns(2)
                            if cols[0].button("Send Reply", key=f"btn_{p_id}_{i}", type="primary"):
                                if reply:
                                    # 1. Add the doctor's reply to the chat memory
                                    p['chats'].append({'sender': 'Doctor', 'text': reply, 'status': 'Delivered'})
                                    # 2. Mark the original question as resolved so it disappears from this queue
                                    msg['status'] = 'Resolved'
                                    st.success("Reply sent to patient's dashboard!")
                                    st.rerun()
                                else:
                                    st.warning("Please type a reply before sending.")
                                    
                            if cols[1].button("Mark as Resolved (No Reply)", key=f"res_{p_id}_{i}"):
                                msg['status'] = 'Resolved'
                                st.rerun()
                    st.divider()
                    
            if not has_active_queries:
                st.success("✅ All patient queries have been answered. You are all caught up!")