import streamlit as st
from PIL import Image
import os
import tempfile
from dotenv import load_dotenv
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

from services.ai_service import AIService
from ui.recipe_display import display_recipes

# Load environment variables
load_dotenv()
ORIGINAL_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# Initialize state
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False
if 'api_key_error' not in st.session_state:
    st.session_state.api_key_error = ""
if 'uploaded_img' not in st.session_state:
    st.session_state.uploaded_img = None
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'current_recipes' not in st.session_state:
    st.session_state.current_recipes = []

# Page layout
st.set_page_config(page_title="🍳 AI Chef Assistant", layout="wide")
st.title("🍳 AI Chef Assistant")

# ===== API KEY MANAGEMENT =====
st.sidebar.header("🔑 Gemini API Key Setup")
user_api_key = st.sidebar.text_input(
    "Enter your Gemini API Key:",
    type="password",
    help="Get your key from https://aistudio.google.com/app/apikey"
)

# Use key priority: 1. User key 2. Original key
active_api_key = user_api_key if user_api_key else ORIGINAL_GEMINI_KEY

# Initialize AI Service
ai_service = None
try:
    ai_service = AIService(active_api_key)
    st.session_state.api_key_valid = True
    st.session_state.api_key_error = ""
    key_source = "your input" if user_api_key else "default"
    st.sidebar.success(f"✅ Using {key_source} API key")
except Exception as e:
    st.session_state.api_key_valid = False
    st.session_state.api_key_error = f"API Error: {str(e)}"
    st.sidebar.error(f"❌ {st.session_state.api_key_error}")
    st.sidebar.warning("Please enter a valid Gemini API key to use the app")

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file to text"""
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# ===== MAIN APP CONTENT =====
if st.session_state.api_key_valid:
    st.subheader("Describe ingredients via voice OR upload a photo")
    
    # Create two columns for input options
    img_col, voice_col = st.columns(2)

    # ===== IMAGE INPUT SECTION =====
    with img_col:
        st.header("📷 Image Input")
        uploaded_img = st.file_uploader(
            "Upload ingredients photo:", 
            type=["jpg", "png", "jpeg"]
        )
        
        if uploaded_img:
            st.session_state.uploaded_img = uploaded_img
            st.image(uploaded_img, caption="Your ingredients", width=300)
        else:
            st.session_state.uploaded_img = None

    # ===== VOICE INPUT SECTION =====
    with voice_col:
        st.header("🎤 Voice Command")
        
        # Option 1: Upload audio file
        audio_file = st.file_uploader("Upload audio file:", type=["wav", "mp3", "m4a"])
        
        # Option 2: Record audio directly
        st.write("Or record your voice:")
        audio_bytes = audio_recorder(text="", recording_color="#e8b62c", neutral_color="#6aa36f")
        
        if audio_bytes:
            st.session_state.audio_bytes = audio_bytes
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            st.audio(audio_bytes, format="audio/wav")
            st.session_state.transcribed_text = transcribe_audio(tmp_path)
        
        elif audio_file:
            st.session_state.audio_file = audio_file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            st.audio(audio_file.read(), format="audio/wav")
            st.session_state.transcribed_text = transcribe_audio(tmp_path)

        if st.session_state.transcribed_text:
            st.success(f"Transcribed: {st.session_state.transcribed_text}")

    # ===== COMMON INPUTS =====
    st.divider()
    allergies = st.text_input("Allergies or foods to avoid:", placeholder="nuts, dairy, gluten...")
    prep_time = st.slider("Max preparation time (minutes):", 10, 120, 30)

    # ===== RECIPE GENERATION =====
    if st.button("✨ Create Recipe!"):
        try:
            with st.spinner("🧠 AI Chef is thinking..."):
                if st.session_state.uploaded_img:
                    img = Image.open(st.session_state.uploaded_img)
                    st.session_state.current_recipes = ai_service.generate_recipes_from_image(
                        image=img,
                        allergies=allergies,
                        max_time=prep_time
                    )
                elif st.session_state.transcribed_text:
                    st.session_state.current_recipes = ai_service.generate_recipes_from_text(
                        ingredients_text=st.session_state.transcribed_text,
                        allergies=allergies,
                        max_time=prep_time
                    )
                else:
                    st.warning("Please provide ingredients via image or voice!")
        except Exception as e:
            st.error(f"Recipe generation failed: {str(e)}")
            st.error("Please check your API key or try again later")

    # Display recipes if they exist
    if st.session_state.current_recipes:
        display_recipes(st.session_state.current_recipes)

else:
    st.warning("Please enter a valid Gemini API key in the sidebar to use the cooking assistant")
    st.info(""" **How to get an API key:** 1. Go to [Google AI Studio](https://aistudio.google.com/) 2. Click "Get API key" in the left sidebar 3. Create API key under "Create API key in new project" 4. Copy and paste the key into the sidebar input """)
    st.image("https://i.imgur.com/H3j5g4W.png", caption="Where to find Gemini API key", width=500)


