"""
Voice-Activated SOS System — Desktop Version
----------------------------------------------
Listens continuously through your microphone for trigger words
(help, sos, emergency, mayday). When detected, starts a countdown
that the user can cancel; otherwise it sounds an alarm and sends
an SMS with an approximate location via Twilio.

Setup:
  1. pip install speechrecognition pyaudio twilio requests --break-system-packages
     (On Linux you may also need: sudo apt-get install portaudio19-dev)
  2. Fill in the CONFIG section below with your own values.
  3. Run: python sos_system.py
"""

import speech_recognition as sr
import threading
import time
import datetime
from twilio.rest import Client

# ── CONFIG ────────────────────────────────────────────────────────
KEYWORDS           = ['help', 'sos', 'emergency', 'mayday']
COUNTDOWN_SEC       = 5
TWILIO_SID         = 'ACxxxxxxxxxxxxxxxx'      # from twilio.com/console
TWILIO_TOKEN       = 'your_auth_token'         # from twilio.com/console
TWILIO_FROM        = '+1XXXXXXXXXX'            # your Twilio phone number
EMERGENCY_CONTACTS = ['+91XXXXXXXXXX']         # numbers to alert
# ─────────────────────────────────────────────────────────────────

sos_pending  = False
cancel_event = threading.Event()
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)


def send_sms(location_str):
    msg = f"SOS ALERT\nTime: {datetime.datetime.now()}\nLocation: {location_str}"
    for number in EMERGENCY_CONTACTS:
        twilio_client.messages.create(body=msg, from_=TWILIO_FROM, to=number)
        print(f"SMS sent to {number}")


def get_location():
    """Rough location via IP lookup. For a real device, swap in GPS hardware."""
    import requests
    try:
        r = requests.get('https://ipinfo.io/json', timeout=5)
        data = r.json()
        loc = data.get('loc', '')
        city = data.get('city', '')
        return f"https://maps.google.com/?q={loc} ({city})" if loc else "Unknown"
    except Exception:
        return "Location unavailable"


def play_alarm():
    for _ in range(5):
        print('\a', end='', flush=True)
        time.sleep(0.3)


def trigger_sos():
    print("\nSOS TRIGGERED")
    location = get_location()
    print(f"Location: {location}")
    play_alarm()
    send_sms(location)


def sos_countdown():
    global sos_pending
    cancel_event.clear()
    print(f"\nKeyword detected. Triggering in {COUNTDOWN_SEC} seconds.")
    print("Type 'cancel' and press Enter to abort.")

    for i in range(COUNTDOWN_SEC, 0, -1):
        if cancel_event.is_set():
            print("SOS cancelled.")
            sos_pending = False
            return
        print(f"  {i}...")
        time.sleep(1)

    trigger_sos()
    sos_pending = False


def keyword_detected(transcript):
    global sos_pending
    if sos_pending:
        return
    transcript = transcript.lower()
    if any(kw in transcript for kw in KEYWORDS):
        sos_pending = True
        threading.Thread(target=sos_countdown, daemon=True).start()


def listen_for_cancel():
    while True:
        try:
            cmd = input()
            if cmd.strip().lower() == 'cancel':
                cancel_event.set()
        except EOFError:
            break


def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

    print("Listening for SOS keywords:", KEYWORDS)
    threading.Thread(target=listen_for_cancel, daemon=True).start()

    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                transcript = recognizer.recognize_google(audio)
                print(f"Heard: {transcript}")
                keyword_detected(transcript)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"API error: {e}")


if __name__ == '__main__':
    main()
