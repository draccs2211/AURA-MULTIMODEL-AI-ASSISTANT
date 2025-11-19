# --- Standard Library ---
import os
import re
import time
import uuid
import queue
import threading
import subprocess
import smtplib
import webbrowser
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Third-Party Libraries ---
import cv2
import pygame
import requests
import numpy as np
import face_recognition
import pywhatkit as kit
import speech_recognition as sr
from gtts import gTTS
from PIL import Image
from googletrans import Translator
import wolframalpha

# --- Local Modules ---
from face_auth import face_authenticate
from smart_notifications import smart_notify_loop
from calender_helper import add_event_to_calendar, read_events_for_day








WOLFRAM_API_KEY = "GR2YRGEQ6A"  # Replace with your actual App ID
voice_paused = False
NEWS_API_KEY="3703e043610c439abfa642d1809bf083"
WEATHER_API_KEY="cc5c4f45d6feefa3c46c408cd077ecae"
USE_TEXT_INPUT =False #for development phase


def speak(text):
    print(f"🗣️ JARVIS: {text}")
    try:
        filename = "voice.mp3"
        tts = gTTS(text)
        tts.save(filename)

        while not os.path.exists(filename):
            time.sleep(0.1)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(filename)

    except Exception as e:
        print(f"❌ Error in speak(): {e}")

   


# ---- LISTEN FUNCTION ----
def listen():
    global voice_paused
    if voice_paused:
        return ""
    if USE_TEXT_INPUT:
        return input(" Enter your command: ").strip().lower()
    else:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
                return recognizer.recognize_google(audio).lower()
            except:
                speak("Sorry, I didn’t catch that.")
                return ""
notif_thread = threading.Thread(target=smart_notify_loop, args=(speak,), daemon=True)
notif_thread.start()




# COMMAND HANDLER 
def process_command(command):
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://www.linkedin.com")
    elif "open chatgpt" in command:
        speak("Opening ChatGPT for you.")
        webbrowser.open("https://chatgpt.com")
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "play" in command:
        play_on_youtube(command)
    elif "search" in command and "on google" in command:
        google_search(command)

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    elif 'news' in command:
        fetch_news()
    elif 'weather' in command:
        get_weather()
    elif "open" in command:
       open_application(command)
       
    elif "take a note" in command:
        take_note()
    elif "translate" in command:
        translate_text(command)
    elif "send whatsapp" in command:
        whatsmmsg()

    
    elif "create calendar event" in command or "schedule meeting" in command or "add event" in command:
        speak("What's the event title?")
        title = listen()

        speak("Please say the date in YYYY-MM-DD format.")
        date = listen()

        speak("Please say the time in HH:MM 24-hour format.")
        time = listen()

        speak("How long is the event in minutes?")
        duration_str = listen()
        try:
            duration = int(''.join(filter(str.isdigit, duration_str)))
        except:
            speak("Sorry, I couldn't understand the duration.")
            duration = 30

        speak("Adding your event to Google Calendar...")
        success, result = add_event_to_calendar(title, date, time, duration)

        if success:
            speak("Event created successfully!")
            print("Event link:", result)
        else:
            speak("I couldn't create the event. Please try again.")
            print("Error:", result)


    elif "show events" in command or "read calendar" in command:
        speak("For which date? Say the date in YYYY-MM-DD format.")
        date = listen()
        try:
            events = read_events_for_day(date)
            speak(events)
        except:
            speak("Sorry, I couldn't fetch events.")


    



   



       
    elif any(x in command for x in ["calculate", "what is", "who is", "square root", "value of", "convert"]):
        result = ask_wolfram(command)
        if result:
            speak(result)
        else:
            speak("WolframAlpha couldn't answer that. Let me check Google.")
            google_result = google_search(command)
            speak(google_result)
   

    

    

    elif "send an email to" in command:
        try:
            # Extract email and message
            match = re.search(r"send an email to (.+?) saying ['\"](.+?)['\"]", command)
            if match:
                recipient = match.group(1).strip()
                message = match.group(2).strip()
                send_email(recipient, message)
            else:
                speak("Sorry, I didn't catch the full email command.")
        except Exception as e:
            print("❌ Email command error:", e)
            speak("Something went wrong while processing the email.")


        
    else:
        speak("Sorry, I don't know how to do that yet.")





# ---- WAKE WORD LISTENER ----
def wait_for_wake_word():
    speak("I didn't recognize your face. Say  the 'PASSWORD' to activate.")
    while True:
        command = listen()
        if "aura" in command:
            speak("HELLO I AM AURA. What can I do for you?")
            return



def fetch_news():
    import requests
    speak("Fetching the latest headlines...")

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",             # or "in" for India
        "pageSize": 5,               # get top 5
        "apiKey": NEWS_API_KEY    # replace with your actual key
    }

    response = requests.get(url, params=params)
    data = response.json()
    print("🧪 API Response:", data)

    if data["status"] == "ok" and data["articles"]:
        for i, article in enumerate(data["articles"], 1):
            speak(f"Headline {i}: {article['title']}")
    else:
        speak("Sorry, no news headlines available right now.")



def get_weather(city="Lucknow"):
    speak(f"Getting the weather for {city}.")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        print("🌦️ Weather API Response:", data)

        if data.get("cod") != 200:
            speak("Sorry, I couldn't fetch the weather.")
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        report = (
            f"The current temperature in {city} is {temp}°C. "
            f"Weather condition is {description}. "
            f"Humidity is {humidity}% and wind speed is {wind_speed} meters per second."
        )
        speak(report)

    except Exception as e:
        print(" Error fetching weather:", e)
        speak("Something went wrong while getting the weather.")
def play_on_youtube(command):
    song = command.replace("play", "").strip()
    if song:
        speak(f"Playing {song} on YouTube")
        kit.playonyt(song)
    else:
        speak("Please specify what you'd like me to play.")

def google_search(command):
    query = command.lower().replace("search", "").replace("on google", "").strip()
    if query:
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        speak("Please say what you want me to search on Google.")



EMAIL_ADDRESS = "draccs22114@gmail.com"
EMAIL_PASSWORD = "rbfm wwio jcnk gsot" 

def send_email(to_address, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        msg['Subject'] = "Message from JARVIS"
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        speak("Email has been sent successfully.")
    except Exception as e:
        print(" Error:", e)
        speak("Failed to send the email.")


def open_application(command):
    command = command.lower()

    if "notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "chrome" in command:
        speak("Opening Google Chrome")
        # If Chrome is not in PATH, give full path like below:
        # subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        os.system("start chrome")

    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("start calc")
    elif "vs code" in command:
        speak("opening vs code")
        os.system("code")
    elif "whatsapp" in command:
        speak('opening whatsapp')
        os.system("start whatsapp:")
    elif "command prompt" in command or "cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")
    elif 'computer setting' or 'pc setting' or 'mobile settings' in command:
        speak("opening setting")
        os.system("start ms-settings:")
    
    

    else:
        speak("Sorry, I don't know how to open that application.")
        
import pywhatkit

def ask_wolfram(query):
    url = "https://api.wolframalpha.com/v2/query"
    params = {
        "input": query,
        "appid": WOLFRAM_API_KEY,
        "output": "JSON"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        print("🧪 API JSON:", data)  # debug

        pods = data["queryresult"].get("pods", [])
        for pod in pods:
            if pod["title"].lower() in ["result", "definition", "basic information"]:
                for subpod in pod.get("subpods", []):
                    answer = subpod.get("plaintext")
                    if answer:
                        print("🗣️ JARVIS:", answer)
                        return answer

        # Fallback to Google if no direct answer
        print("🗣️ JARVIS: No answer from WolframAlpha. Trying Google search...")
        pywhatkit.search(query)
        return "I couldn't find a direct answer. So, I searched it on Google for you."

    except Exception as e:
        print("⚠️ Wolfram Error:", e)
        pywhatkit.search(query)
        return "There was an error, so I searched it on Google instead."
def take_note():
    speak("What should I write?")
    note = listen()
    if note:
        with open("notes.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {note}\n")
        speak("Note saved.")

def translate_text(command):
    pattern = r"translate ['\"]?(.+?)['\"]? to (\w+)"
    match = re.search(pattern, command.lower())

    if match:
        text_to_translate = match.group(1)
        target_language = match.group(2)

        translator = Translator()
        try:
            translated = translator.translate(text_to_translate, dest=target_language)
            print(f"🈯 Translated: {translated.text}")
            speak(f"In {target_language}, you would say: {translated.text}")
        except Exception as e:
            speak("Sorry, I couldn't translate that.")
            print("Translation Error:", e)
    else:
        speak("Sorry, please say something like: Translate 'Hello' to Spanish.")

def whatsmmsg():
    speak("Please say the recipient's number")
    number_input = listen()

    
    number = number_input.lower().replace("plus", "+").replace(" ", "")
    number = ''.join(c for c in number if c in "+919336943754")

    if not number.startswith("+") or len(number) < 10:
        speak("That doesn't seem like a valid number. Please try again.")
        return

    speak("What message should I send?")
    message = listen()

    if not message:
        speak("No message received. Please try again.")
        return

    now = datetime.now()
    hour = now.hour
    minute = now.minute + 2

    try:
        speak(f"Scheduling WhatsApp message to  in 2 minutes.")
        kit.sendwhatmsg(number, message, hour, minute)
        speak("Your WhatsApp message has been scheduled.")
    except Exception as e:
        print("Error:", e)
        speak("Sorry, something went wrong while sending the message.")





def text_input_loop():
    while True:
        command = input("⌨️ Type your command: ").strip().lower()
        if command:
            process_command(command)



if __name__ == "__main__":
    if face_authenticate(speak=speak):
        from gesture_controller import gesture_loop

        # Start gesture detection in background
        threading.Thread(target=gesture_loop, daemon=True).start()

        # ⛔ Text input temporarily disabled
        threading.Thread(target=text_input_loop, daemon=True).start()

        time.sleep(2)

        # Voice command loop (runs in main thread)
        while True:
            command = listen()
            if command:
                process_command(command)
    else:
        wait_for_wake_word()
        from gesture_controller import gesture_loop

        threading.Thread(target=gesture_loop, daemon=True).start()

        threading.Thread(target=text_input_loop, daemon=True).start()

        time.sleep(2)

        while True:
            command = listen()
            if command:
                process_command(command)
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
