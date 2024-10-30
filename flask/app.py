import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from audio.audio_record import AudioRecorder
from audio.transcribe_audio import transcribe_audio
from audio.analyze_text_for_image import analyze_text_for_image
from image.generate_image_flux import generate_image_flux
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # HTML file we'll create for the UI

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recorder
    recorder = AudioRecorder()
    recorder.start_recording()
    return jsonify({"status": "recording started"})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    filename = f"recording_{int(time.time())}.wav"
    success = recorder.stop_recording(filename)
    recorder.close()
    
    if success:
        text = transcribe_audio(filename)
        if text:
            prompt = analyze_text_for_image(text)
            if prompt != "none":
                image_path = generate_image_flux(prompt)
                return jsonify({"status": "recording stopped", "image": image_path})
    return jsonify({"status": "no audio frames"})

if __name__ == '__main__':
    app.run(debug=True)
