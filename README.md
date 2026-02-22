# Voice Transcription System

A web-based speech-to-text application built with Flask that converts audio files into text using Google's Speech Recognition API.

## Features

- **Audio File Upload** — Upload audio files via drag & drop or file browser
- **Speech-to-Text** — Transcribes audio using Google Speech Recognition
- **Real-time Feedback** — Loading spinner and inline result display
- **Modern UI** — Glassmorphism design with a blue/sky theme

## Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Backend   | Flask (Python)      |
| Frontend  | HTML, CSS, JavaScript |
| Speech Engine | Google Speech Recognition via `SpeechRecognition` library |

## Project Structure

```
voice_system/
├── app.py              # Flask application with routes and frontend
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment
└── README.md           # Project documentation
```

## Installation

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

## API Endpoint

### `POST /transcribe`

Accepts an audio file and returns the transcribed text.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `audio` — the audio file (.wav, .mp3, etc.)

**Response (Success):**
```json
{
  "transcribed_text": "Hello, how are you?"
}
```

**Response (Error):**
```json
{
  "error": "Could not understand audio"
}
```

## Dependencies

- `flask` — Web framework
- `numpy` — Numerical computing
- `vosk` — Offline speech recognition model
- `SpeechRecognition` — Speech-to-text interface
- `pyaudio` — Audio I/O
