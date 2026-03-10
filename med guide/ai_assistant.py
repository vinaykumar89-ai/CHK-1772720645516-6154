import streamlit as st
import google.generativeai as genai
from PIL import Image
from pyzbar.pyzbar import decode
import datetime

# ==========================================
# 🔑 PASTE YOUR GEMINI API KEY HERE
# ==========================================
GEMINI_API_KEY = "YOUR_API_KEY_GOES_HERE"

def translate_with_gemini(text, target_lang):
    """Translates doctor messages into the patient's language using Gemini."""
    if GEMINI_API_KEY == "YOUR_API_KEY_GOES_HERE":
        return text 
        
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Translate the following medical advice into {target_lang}. Only return the translated text. Do not add any conversational filler or formatting.\n\nMedical Advice: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return text 

def process_voice_message(audio_bytes):
    """Listens to the patient's regional audio and translates it to English for the doctor."""
    if GEMINI_API_KEY == "YOUR_API_KEY_GOES_HERE":
        return "⚠️ API Key missing. Please configure it in ai_assistant.py."
        
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Listen to this patient's audio. Transcribe it, and translate it into clear English for a doctor to read. Return ONLY the English translation. Do not include any extra text."
        
        response = model.generate_content([
            prompt, 
            {"mime_type": "audio/wav", "data": audio_bytes}
        ])
        return response.text.strip()
    except Exception as e:
        return f"Audio processing error: {e}"

def render_smart_assistant(username):
    p_data = st.session_state.patients[username]
    lang = st.session_state.language
    
    st.subheader("🤖 Smart Assistant & Scanner")
    st.caption("Ask questions, attach medical reports, or scan a medicine barcode directly here.")
    
    if GEMINI_API_KEY == "YOUR_API_KEY_GOES_HERE":
        st.warning("⚠️ Please insert your Gemini API Key in ai_assistant.py to enable the AI.")
        return
        
    genai.configure(api_key=GEMINI_API_KEY)

    system_instruction = """
    You are an empathetic, elder-friendly medical assistant.
    
    RULE 1 - BARCODES/MEDICINES: If the user provides a barcode number or asks about a medicine, format your answer strictly as:
    ### 💊 [Medicine Name]
    - **Uses:** [Brief explanation]
    - **Harms/Side Effects:** [Brief explanation]
    - **Alternative Home Remedy:** [Suggest a safe, natural alternative if applicable].
    
    RULE 2 - DISEASES: If asked about a disease or symptom, DO NOT CAUSE PANIC. Use a calm, reassuring tone. Explain it simply. 
    YOU MUST END YOUR RESPONSE WITH THIS EXACT SENTENCE: 
    "**Disclaimer: Internet searches are not 100% true. Please visit your nearest doctor.**"
    
    RULE 3 - FILES/IMAGES: If the user uploads a document or prescription, read it thoroughly and explain what it means in very simple terms for a senior citizen.
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

    if "ai_chats" not in st.session_state:
        st.session_state.ai_chats = []

    # --- UI: The Omni-Input Area ---
    uploaded_file = None
    with st.expander("📷 Scan Medicine Barcode or Attach Report"):
        tab_cam, tab_file = st.tabs(["🎥 Use Camera", "📁 Upload File"])
        with tab_cam:
            cam_img = st.camera_input("Scan your medicine box or document", label_visibility="collapsed")
            if cam_img: uploaded_file = cam_img
        with tab_file:
            file_img = st.file_uploader("Upload an image file", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if file_img: uploaded_file = file_img

    # --- RENDER CHAT HISTORY ---
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.ai_chats:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # --- DOSE CONFIRMATION BUTTON ---
    if st.session_state.get('pending_med_log'):
        time_slot = st.session_state.pending_med_log
        if not p_data['meds'][time_slot]:
            st.info(f"The AI verified your medicine. Would you like to log your {time_slot} dose now?")
            if st.button(f"✅ Confirm taking {time_slot} dose", type="primary"):
                p_data['meds'][time_slot] = True
                st.session_state.speech_queue = f"{time_slot} dose marked as taken."
                st.session_state.pending_med_log = None 
                st.rerun()

    # --- THE CHAT BAR & ACTION LOGIC ---
    analyze_image_btn = False
    if uploaded_file:
        st.success("✅ Image attached! Type a question below, or click the button to scan it instantly.")
        analyze_image_btn = st.button("🔍 Analyze Image / Scan Barcode", use_container_width=True)

    user_query = st.chat_input("Ask about a medicine, disease, or process the attached file...")

    if user_query or analyze_image_btn:
        prompt = user_query if user_query else ""
        img_obj = None
        barcode_data = None
        
        if uploaded_file:
            img_obj = Image.open(uploaded_file)
            decoded = decode(img_obj)
            
            if decoded:
                barcode_data = decoded[0].data.decode('utf-8')
                if not prompt:
                    prompt = f"I scanned a medicine with barcode {barcode_data}. Please identify this medicine and explain its uses."
            else:
                if not prompt:
                    prompt = "Please thoroughly read and explain this medical document or image in simple terms."

        display_prompt = prompt if prompt else "Analyze image."
        st.session_state.ai_chats.append({"role": "user", "content": display_prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.write(display_prompt)
                if uploaded_file:
                    st.caption("(Image Attached)")

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    try:
                        if img_obj:
                            response = model.generate_content([prompt, img_obj])
                        else:
                            response = model.generate_content(prompt)
                            
                        st.write(response.text)
                        st.session_state.ai_chats.append({"role": "assistant", "content": response.text})
                        st.session_state.speech_queue = "Analysis complete."
                        
                        if barcode_data:
                            current_hour = datetime.datetime.now().hour
                            time_slot = "Morning"
                            if 12 <= current_hour < 17:
                                time_slot = "Afternoon"
                            elif current_hour >= 17:
                                time_slot = "Night"
                                
                            st.session_state.pending_med_log = time_slot
                            st.rerun() 

                    except Exception as e:
                        st.error(f"Error connecting to AI: {e}")