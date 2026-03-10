import streamlit.components.v1 as components

def speak_text(text, language="English"):
    """
    Triggers the browser's built-in Text-to-Speech engine.
    Maps your app's UI languages to standard browser voice codes.
    """
    lang_codes = {
        "English": "en-IN",  # Indian English accent
        "Hindi": "hi-IN",    # Hindi voice
        "Marathi": "mr-IN",  # Marathi voice
        "Kannada": "kn-IN"   # Kannada voice
    }
    
    voice_code = lang_codes.get(language, "en-IN")
    
    js_code = f"""
    <script>
        // Stop any currently playing audio so they don't overlap
        window.parent.speechSynthesis.cancel();
        
        // Create the speech request
        let utterance = new SpeechSynthesisUtterance("{text}");
        utterance.lang = "{voice_code}";
        utterance.rate = 0.85; // Slightly slower speed for elderly users
        
        // Speak!
        window.parent.speechSynthesis.speak(utterance);
    </script>
    """
    
    # Render the invisible script block
    components.html(js_code, height=0, width=0)