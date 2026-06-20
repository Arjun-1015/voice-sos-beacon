# Voice SOS Beacon

A voice-activated personal safety system. Say a trigger word, and after a short countdown — which you can cancel — it sends an SMS with your location to your emergency contacts.

Includes two versions:
- **Web app** (`public/`) — runs in Chrome/Edge using the Web Speech API, with a Node.js backend for sending SMS via Twilio.
- **Desktop/Python script** (`sos_system.py`) — a standalone version for always-on use on a laptop or Raspberry Pi.

## Features

- Continuous voice listening for keywords: `help`, `sos`, `emergency`, `mayday`
- 5-second cancellable countdown before triggering, to avoid false alarms
- Sends an SMS via Twilio with an approximate location and timestamp
- Audible alarm tone on trigger
- Live event log of everything the recognizer hears

## Prerequisites

- [Node.js](https://nodejs.org) (for the web app)
- [Python 3](https://www.python.org/downloads/) (for the desktop version, optional)
- A [Twilio](https://www.twilio.com/try-twilio) account (free trial works) with:
  - Account SID
  - Auth Token
  - A Twilio phone number with SMS capability
  - Your destination number added under **Verified Caller IDs** (required on trial accounts)
- Google Chrome or Microsoft Edge (the Web Speech API isn't supported in Firefox/Safari)

## Setup — Web App

1. Clone the repo:
   ```bash
   git clone https://github.com/Arjun-1015/voice-sos-beacon.git
   cd voice-sos-beacon
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the project root (this is gitignored — you must create your own):
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_FROM_NUMBER=+1XXXXXXXXXX
   ```

4. Open `public/index.html` and set your emergency contact number:
   ```js
   const CONTACTS = ['+91XXXXXXXXXX'];
   ```

5. Start the server:
   ```bash
   node server.js
   ```

6. Open `http://localhost:3000` in Chrome or Edge, click **Start Listening**, and grant microphone access.

## Setup — Desktop / Python Version

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   On Windows, if `pyaudio` fails to build, use:
   ```bash
   pip install pipwin
   python -m pipwin install pyaudio
   ```

2. Edit the `CONFIG` section at the top of `sos_system.py` with your Twilio credentials and contact numbers.

3. Run it:
   ```bash
   python sos_system.py
   ```

## Project Structure

```
voice-sos-beacon/
├── public/
│   ├── index.html       # frontend UI
│   └── style.css        # styling
├── server.js            # Express backend, sends SMS via Twilio
├── package.json
├── sos_system.py         # standalone desktop/Python version
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## Security Note

Never commit your `.env` file. It contains live Twilio credentials that could be used to send SMS (and incur charges) on your account. This repo's `.gitignore` already excludes it — keep it that way.

## Known Limitations

- Location is approximate (IP-based in the Python version, browser geolocation in the web version) — not precise GPS.
- On the web version, after a real SOS is triggered (not cancelled), voice recognition stops auto-restarting — refresh the page to re-arm it.
- Twilio trial accounts can only send SMS to verified numbers and prepend a "sent from a trial account" notice to every message.

## License

This project is provided as-is for personal/educational use.
