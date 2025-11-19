# smart_notifications.py
import psutil
import socket
import threading
import time
import platform
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes  

comtypes.CoInitialize()

def speak(message, tts_func):
    print(f"🔔 Notification: {message}")
    tts_func(message)  # You can replace with gTTS or pyttsx3 call

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def get_volume_status():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_vol = volume.GetMasterVolumeLevelScalar()  # 0.0 to 1.0
    mute = volume.GetMute()
    return current_vol, mute

def smart_notify_loop(tts_func):
    import psutil
    import socket
    import time
    import comtypes
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    # ✅ Initialize COM *in the same thread*
    comtypes.CoInitialize()

    # State tracking
    notified = {
        "low_battery": False,
        "no_internet": False,
        "muted": False,
    }

    def speak_notification(msg):
        print(f"🔔 {msg}")
        tts_func(msg)

    def is_connected():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def get_volume_status():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_vol = volume.GetMasterVolumeLevelScalar()  # 0.0 to 1.0
        mute = volume.GetMute()
        return current_vol, mute

    while True:
        # Battery check
        battery = psutil.sensors_battery()
        if battery and battery.percent < 20 and not notified["low_battery"]:
            speak_notification("Battery is low. Please plug in the charger.")
            notified["low_battery"] = True
        elif battery and battery.percent >= 20:
            notified["low_battery"] = False

        # Internet check
        if not is_connected() and not notified["no_internet"]:
            speak_notification("Internet is disconnected.")
            notified["no_internet"] = True
        elif is_connected():
            notified["no_internet"] = False

        # Volume check
        try:
            vol_level, is_muted = get_volume_status()
            if (is_muted or vol_level < 0.01) and not notified["muted"]:
                speak_notification("Your volume is muted.")
                notified["muted"] = True
            elif vol_level > 0.01 and not is_muted:
                notified["muted"] = False
        except Exception as e:
            print(f"❌ Volume check failed: {e}")

        time.sleep(15)
        comtypes.CoUninitialize()
