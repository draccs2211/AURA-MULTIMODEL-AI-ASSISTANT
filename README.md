AURA – Multimodal AI Assistant

AURA is an advanced multimodal personal assistant built in Python that supports
Voice Commands, Gesture Control, Face Authentication, and Text Input — all working together in real time.

AURA can open applications, send WhatsApp messages, fetch news & weather, create calendar events, translate languages, authenticate user face, and perform AI-powered reasoning using multiple APIs.

This project is designed to be a JARVIS-like intelligent assistant with more than 15 smart modules integrated.
Key Features
🔊 1. Voice Interaction

Uses Google Speech Recognition

Executes commands like:

Open YouTube, Google, LinkedIn, ChatGPT

Search on Google

Play songs on YouTube

Tell the time

Fetch news

Fetch weather

Perform calculations using WolframAlpha

👁️ 2. Face Authentication

Uses face_recognition library

Only the registered user's face can activate AURA

Acts as a biometric wake trigger

✋ 3. Gesture Control

Uses Hand Detection & Tracking

Support for:

Play/Pause voice

Control media

Trigger commands

Hands-free operation

⌨️ 4. Text Mode

AURA can also take text input for debugging or silent use.

🔗 5. API-Powered Modules

AURA integrates over 15 smart features:

Feature	Libraries Used
Weather	OpenWeatherMap API
News	NewsAPI
WhatsApp Sender	PyWhatKit
Play YouTube	PyWhatKit
Email Sender	smtplib + Gmail SMTP
Calendar Automation	Google Calendar API
Translator	googletrans / deep-translator
TTS Voice Output	gTTS + Pygame
Computer Apps Launcher	os / subprocess
Math & Facts Queries	WolframAlpha API
📁 6. Modular Code Structure

AURA supports clean modular files:

jarvis.py
gui/
    main_gui.py
    chat_panel.py
    logs_panel.py
    quick_actions.py
    status_panel.py
utils/
    speak.py
smart_notifications.py
gesture_controller.py
face_auth.py
configs.py

🧠 Supported Commands (Examples)
✔ System Operations

"Open Chrome"

"Open Notepad"

"Open VS Code"

"Open WhatsApp"

✔ Online Search

"Search AI internships on Google"

"Play Arijit Singh songs on YouTube"

✔ Productivity

"Create calendar event"

"Take a note"

"Read notes"

✔ AI Tools

"Calculate 29 × 44"

"What is the square root of 67?"

"Who is the president of India?"

✔ Integrations

"Send WhatsApp message"

"Send an email to ___ saying ___"

⚡ Tech Stack

Python 3.9+

OpenCV

face_recognition

SpeechRecognition

Google Text-to-Speech (gTTS)

Pygame

WolframAlpha API

Google APIs
Installation
1️⃣ Clone the repository
git clone https://github.com/draccs2211/AURA-MULTIMODEL-AI-ASSISTANT.git

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run AURA
python jarvis.py

⚠️ Before Running

Create a .env file and add your API keys:

WOLFRAM_API_KEY=your_key
NEWS_API_KEY=your_key
WEATHER_API_KEY=your_key
GOOGLE_API_CLIENT_ID=your_client_id
OPENAI_API_KEY=your_api_key (optional)
Future Improvements

✔ Add a full Desktop GUI

✔ Integrate OpenAI Realtime API

✔ Add LLM Chat mode to GUI

✔ Create a launcher EXE

✔ Improve gesture recognition

🤝 Contributions

Pull requests are welcome!
If you want to improve a module or fix a bug—feel free to contribute.

⭐ Star this project

If you found this useful, consider ⭐ starring the repo!


