from flask import Flask, render_template, request
import speech_recognition as sr
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"

@app.route("/", methods=["GET", "POST"])
def index():
    transcription = ""

    if request.method == "POST":
        file = request.files["audio"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        transcription = transcribe_audio(file_path)

    return render_template("index.html", transcription=transcription)

if __name__ == "__main__":
    app.run(debug=True)