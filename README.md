# 🍳 AI Chef Assistant

An intelligent cooking assistant that generates personalized recipes based on your available ingredients. Simply take a photo of your ingredients or describe them by voice, and let AI create delicious recipes tailored to your needs.

## ✨ Features

- **Multiple Input Methods**

  - 📷 Upload photos of ingredients
  - 🎤 Voice command input
  - 🎙️ Audio file upload support (WAV, MP3, M4A)

- **Smart Recipe Generation**

  - 🤖 AI-powered recipe creation
  - 📝 Multiple recipe suggestions
  - ⚡ Real-time generation
  - 🔄 Considers dietary restrictions
  - ⏱️ Respects time constraints

- **User-Friendly Interface**
  - 👀 Clean, modern design
  - 📱 Responsive layout
  - 💾 Save recipes as text files
  - 📋 Clear ingredient lists
  - 📝 Step-by-step instructions

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-powered-cooking-assistant.git
cd ai-powered-cooking-assistant
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the App

1. Start the Streamlit app:

```bash
streamlit run app.py
```

2. Open your browser and navigate to the displayed URL (typically `http://localhost:8501`)

## 📖 Usage

1. **API Key Setup**

   - Enter your Gemini API key in the sidebar
   - Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)

2. **Input Ingredients**

   - Option 1: Upload a photo of your ingredients
   - Option 2: Use voice command to describe ingredients
   - Option 3: Upload an audio file with ingredient description

3. **Specify Preferences**

   - Enter any allergies or foods to avoid
   - Set maximum preparation time

4. **Generate Recipes**
   - Click "Create Recipe!"
   - View multiple recipe suggestions
   - Save preferred recipes

## 🏗️ Project Structure

```
ai-powered-cooking-assistant/
├── app.py                 # Main Streamlit application
├── models/
│   └── recipe.py         # Recipe data model and utilities
├── services/
│   └── ai_service.py     # AI service for recipe generation
├── ui/
│   └── recipe_display.py # UI components and styling
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Google Gemini AI**: Recipe generation
- **SpeechRecognition**: Voice input processing
- **PIL**: Image processing
- **Python-dotenv**: Environment management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering recipe generation
- Streamlit for the amazing web framework
- All contributors and users of this project
