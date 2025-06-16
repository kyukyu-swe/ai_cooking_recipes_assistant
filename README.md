# 🍳 AI Chef Assistant

**AI Chef Assistant** is a Streamlit-based web app that helps users generate creative recipes using either a photo of ingredients or a voice command. Powered by Google's Gemini AI, it provides personalized recipes while considering allergies and time constraints.

---

## 🚀 Features

- 🖼️ **Image Input**: Upload a photo of your ingredients to generate a recipe.
- 🎤 **Voice Input**: Speak your ingredients or upload an audio file.
- ⚠️ **Allergy Consideration**: Specify allergies to avoid restricted ingredients.
- ⏱️ **Time Constraints**: Set maximum preparation time for convenience.
- 📋 **Recipe Details**: Includes name, ingredients, steps, prep time, calories, and a chef's tip.
- 💾 **Save Recipes**: Store multiple recipes in your personal recipe book.

---

## 📦 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following:

```env
GEMINI_API_KEY=your_google_generativeai_api_key
```

Make sure `.env` is in `.gitignore` to avoid exposing your API key.

---

## 🛠️ Run the App

Run the Streamlit app using:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
AI_POWERED_COOKING_ASSISTANT/
├── app.py               # Main Streamlit app
├── .env                 # Environment variables (not committed)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── cooking/             # (Ignored in git, add your own assets/modules here)
```

---

## 📌 Notes

- Uses **Google's Gemini 2.0 Flash** for fast and efficient content generation.
- Audio recognition uses **Google Speech Recognition API** via `speech_recognition`.
- Embedded **audio_recorder_streamlit** for real-time recording.

---

## 🧑‍🍳 Made with ❤️ for foodies and tech lovers!
