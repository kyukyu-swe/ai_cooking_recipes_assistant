import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import tempfile
from dotenv import load_dotenv
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder  # New audio recorder

# Load API keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
st.set_page_config(page_title="🍳 AI Chef Assistant", layout="wide")

# Initialize models
vision_model = genai.GenerativeModel('gemini-2.0-flash')
text_model = genai.GenerativeModel('gemini-2.0-flash')
response = ""

# Page layout
st.title("🍳 AI Chef Assistant")
st.subheader("Describe ingredients via voice OR upload a photo")

# Create two columns for input options
img_col, voice_col = st.columns(2)

# Function for voice transcription
def transcribe_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)  # Using Google's free speech recognition
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# ===== IMAGE INPUT SECTION =====
with img_col:
    st.header("📷 Image Input")
    uploaded_img = st.file_uploader("Upload ingredients photo:", 
                                   type=["jpg", "png", "jpeg"])
    
    # Display uploaded image preview
    if uploaded_img:
        st.image(uploaded_img, caption="Your ingredients", width=300)

# ===== VOICE INPUT SECTION =====
with voice_col:
    st.header("🎤 Voice Command")
    transcribed_text = ""
    
    # Option 1: Upload audio file
    audio_file = st.file_uploader("Upload audio file:", 
                                 type=["wav", "mp3", "m4a"])
    
    # Option 2: Record audio directly
    st.write("Or record your voice:")
    audio_bytes = audio_recorder(text="", recording_color="#e8b62c", neutral_color="#6aa36f")
    
    # Process audio if recorded
    if audio_bytes:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        st.audio(audio_bytes, format="audio/wav")
        transcribed_text = transcribe_audio(tmp_path)
        
    # Process uploaded audio file
    elif audio_file:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        st.audio(audio_file.read(), format="audio/wav")
        transcribed_text = transcribe_audio(tmp_path)
    
    # Display transcription
    if transcribed_text:
        st.success(f"Transcribed: {transcribed_text}")

# ===== COMMON INPUTS =====
st.divider()
allergies = st.text_input("Allergies or foods to avoid:", placeholder="nuts, dairy, gluten...")
prep_time = st.slider("Max preparation time (minutes):", 10, 120, 30)

# ===== RECIPE GENERATION =====
if st.button("✨ Create Recipe!"):
    prompt = f"""
    Create a detailed recipe using ONLY the provided ingredients.
    Important constraints:
    - Strictly use only available ingredients
    - Avoid: {allergies if allergies else 'none'}
    - Max cooking time: {prep_time} minutes
    - Include estimated calories per serving
    
    Output format:
    | Recipe Name | [Creative name] |
    |-------------|-----------------|
    | Ingredients | - [item1]<br>- [item2] |
    | Steps | 1. [step1]<br>2. [step2] |
    | Prep Time | [time] minutes |
    | Calories | [number] per serving |
    | Chef's Tip | [helpful cooking tip] |
    """
    
    if uploaded_img:
        # Process image input
        img = Image.open(uploaded_img)
        response = vision_model.generate_content([prompt, img])
        st.success("Generated from image!")
        st.markdown(response.text)
        
    elif transcribed_text:
        # Process voice input
        voice_prompt = f"{prompt}\n\nAvailable ingredients: {transcribed_text}"
        response = text_model.generate_content(voice_prompt)
        st.success("Generated from voice command!")
        st.markdown(response.text)
        
    else:
        st.warning("Please provide ingredients via image or voice!")

# ===== SAVED RECIPES SECTION =====
if 'recipes' not in st.session_state:
    st.session_state.recipes = []
    
if response and st.button("💾 Save Recipe"):
    st.session_state.recipes.append(response.text)
    st.success("Saved to recipe book!")

if st.session_state.recipes:
    st.divider()
    with st.expander("📚 Saved Recipes"):
        for i, recipe in enumerate(st.session_state.recipes, 1):
            st.subheader(f"Recipe #{i}")
            st.markdown(recipe)