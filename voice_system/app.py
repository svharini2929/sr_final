from flask import Flask, request, jsonify
import speech_recognition as sr
import wave

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Voice Transcription</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a1628, #132e5b, #0e2244);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
            }
            .container {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 48px;
                width: 90%;
                max-width: 520px;
                text-align: center;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            }
            .icon { font-size: 48px; margin-bottom: 16px; }
            h1 {
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            .subtitle {
                color: rgba(255, 255, 255, 0.6);
                font-size: 14px;
                margin-bottom: 32px;
            }
            .upload-area {
                border: 2px dashed rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 40px 24px;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 24px;
                position: relative;
            }
            .upload-area:hover, .upload-area.dragover {
                border-color: #38bdf8;
                background: rgba(56, 189, 248, 0.1);
            }
            .upload-area input[type="file"] {
                position: absolute;
                inset: 0;
                opacity: 0;
                cursor: pointer;
            }
            .upload-icon { font-size: 36px; margin-bottom: 12px; }
            .upload-text { font-size: 15px; color: rgba(255,255,255,0.7); }
            .file-name {
                font-size: 13px;
                color: #38bdf8;
                margin-top: 8px;
                display: none;
            }
            button {
                background: linear-gradient(135deg, #38bdf8, #0ea5e9);
                color: #fff;
                border: none;
                padding: 14px 40px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
            }
            button:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(56, 189, 248, 0.4); }
            button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
            .result {
                margin-top: 24px;
                padding: 20px;
                border-radius: 12px;
                text-align: left;
                font-size: 15px;
                line-height: 1.6;
                display: none;
            }
            .result.success { background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); }
            .result.error { background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); }
            .result-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); margin-bottom: 8px; }
            .spinner { display: none; margin: 24px auto 0; width: 32px; height: 32px; border: 3px solid rgba(255,255,255,0.1); border-top-color: #38bdf8; border-radius: 50%; animation: spin 0.8s linear infinite; }
            @keyframes spin { to { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🎙️</div>
            <h1>Voice Transcription</h1>
            <p class="subtitle">Upload an audio file and get instant text transcription</p>

            <form id="uploadForm">
                <div class="upload-area" id="dropZone">
                    <input type="file" name="audio" id="audioFile" accept="audio/*">
                    <div class="upload-icon">📁</div>
                    <div class="upload-text">Drag & drop your audio file here or click to browse</div>
                    <div class="file-name" id="fileName"></div>
                </div>
                <button type="submit" id="submitBtn" disabled>Transcribe Audio</button>
            </form>

            <div class="spinner" id="spinner"></div>
            <div class="result" id="result">
                <div class="result-label">Transcription</div>
                <div id="resultText"></div>
            </div>
        </div>

        <script>
            const fileInput = document.getElementById('audioFile');
            const fileName = document.getElementById('fileName');
            const submitBtn = document.getElementById('submitBtn');
            const form = document.getElementById('uploadForm');
            const spinner = document.getElementById('spinner');
            const result = document.getElementById('result');
            const resultText = document.getElementById('resultText');
            const dropZone = document.getElementById('dropZone');

            fileInput.addEventListener('change', () => {
                if (fileInput.files.length) {
                    fileName.textContent = fileInput.files[0].name;
                    fileName.style.display = 'block';
                    submitBtn.disabled = false;
                }
            });

            ['dragover', 'dragenter'].forEach(e => {
                dropZone.addEventListener(e, ev => { ev.preventDefault(); dropZone.classList.add('dragover'); });
            });
            ['dragleave', 'drop'].forEach(e => {
                dropZone.addEventListener(e, () => dropZone.classList.remove('dragover'));
            });

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                if (!fileInput.files.length) return;

                submitBtn.disabled = true;
                submitBtn.textContent = 'Transcribing...';
                spinner.style.display = 'block';
                result.style.display = 'none';

                const formData = new FormData();
                formData.append('audio', fileInput.files[0]);

                try {
                    const res = await fetch('/transcribe', { method: 'POST', body: formData });
                    const data = await res.json();

                    result.style.display = 'block';
                    if (data.transcribed_text) {
                        result.className = 'result success';
                        resultText.textContent = data.transcribed_text;
                    } else {
                        result.className = 'result error';
                        resultText.textContent = data.error || 'Something went wrong';
                    }
                } catch (err) {
                    result.style.display = 'block';
                    result.className = 'result error';
                    resultText.textContent = 'Failed to connect to server';
                }

                spinner.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Transcribe Audio';
            });
        </script>
    </body>
    </html>
    '''

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = "temp.wav"
    audio_file.save(file_path)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        return jsonify({
            "transcribed_text": text
        })

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400

    except sr.RequestError:
        return jsonify({"error": "Speech service unavailable"}), 500

if __name__ == '__main__':
    app.run(debug=True)
