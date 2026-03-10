import streamlit as st
from translations import get_text

def doctor_view(username):
    d_data = st.session_state.doctors[username]
    lang = st.session_state.language
    
    st.title(get_text(lang, 'doctor_dash'))
    
    if d_data['appointments']:
        for alert in d_data['appointments']:
            st.warning(f"📅 {alert}")
            
    st.divider()
    
    tab1, tab2 = st.tabs([get_text(lang, 'tab_overview'), get_text(lang, 'tab_queries')])
    my_patients = {k: v for k, v in st.session_state.patients.items() if v['doctor'] == username}
    
    with tab1:
        st.subheader(get_text(lang, 'pat_list'))
        for p_id, p in my_patients.items():
            with st.expander(f"{p['name']} | {get_text(lang, 'missed_pills')}: {p['missed_count']}"):
                cols = st.columns(3)
                cols[0].metric(get_text(lang, 'morning'), get_text(lang, 'taken') if p['meds']['Morning'] else get_text(lang, 'pending'))
                cols[1].metric(get_text(lang, 'afternoon'), get_text(lang, 'taken') if p['meds']['Afternoon'] else get_text(lang, 'pending'))
                cols[2].metric(get_text(lang, 'night'), get_text(lang, 'taken') if p['meds']['Night'] else get_text(lang, 'pending'))
                
                if p['missed_count'] > 2:
                    st.error(get_text(lang, 'high_risk'))
    
    with tab2:
        st.subheader(get_text(lang, 'chat_manage'))
        for p_id, p in my_patients.items():
            unresolved = [c for c in p['chats'] if c['status'] == 'Under Process']
            
            if unresolved:
                st.info(f"{p['name']}")
                for i, msg in enumerate(p['chats']):
                    if msg['status'] == 'Under Process':
                        st.write(f"**Q:** {msg['text']}")
                        
                        reply = st.text_input(get_text(lang, 'type_reply'), key=f"reply_{p_id}_{i}")
                        cols = st.columns(2)
                        
                        if cols[0].button(get_text(lang, 'send_resolve'), key=f"btn_{p_id}_{i}"):
                            p['chats'].append({'sender': 'Doctor', 'text': reply, 'status': 'Delivered'})
                            msg['status'] = 'Resolved'
                            st.rerun()
                        if cols[1].button(get_text(lang, 'mark_resolve'), key=f"res_{p_id}_{i}"):
                            msg['status'] = 'Resolved'
                            st.rerun()
            else:
                st.success(f"{get_text(lang, 'no_pending')} {p['name']}.")