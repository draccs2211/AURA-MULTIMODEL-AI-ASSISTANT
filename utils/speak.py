import os
import time
import pygame
from gtts import gTTS

def speak(text):
    print(f"🗣️ AURA: {text}")
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
