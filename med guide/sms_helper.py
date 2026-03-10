import streamlit as st

def send_emergency_sms(emergency_contact, doctor_name, patient_name, address, disease):
    """Simulates sending an SMS to family and the linked doctor."""
    
    message_body = (
        f"🚨 MEDGUIDE EMERGENCY SOS 🚨\n\n"
        f"Patient {patient_name} has triggered an SOS alert!\n"
        f"Known Conditions: {disease}\n"
        f"Location/Address: {address}\n\n"
        f"Please check on them immediately or dispatch an ambulance."
    )
    
    # Format the recipients list
    recipients = f"Family ({emergency_contact})"
    if doctor_name:
        recipients += f" & {doctor_name}"
        
    st.toast(f"📱 SIMULATION: Alerts dispatched!", icon="✅")
    
    # Display the updated green box showing all recipients
    st.success(f"**Simulated SMS Sent To:** {recipients}\n\n**Message Text:**\n\n{message_body}")
    return True