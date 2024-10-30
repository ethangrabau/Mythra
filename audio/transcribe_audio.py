import speech_recognition as sr
import os
import datetime

# Define the path to the memory file
MEMORY_FILE = 'transcription_memory.txt'

def save_transcription(text):
    """Saves the transcribed text to a file for future reference."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(MEMORY_FILE, 'a') as f:  # 'a' mode opens the file for appending
        f.write(f"[{timestamp}] {text}\n")  # Append the transcription with timestamp
    print(f"Transcription saved to {MEMORY_FILE}")

def transcribe_audio(filename):
    """Transcribes audio from a given file using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)  # Read the entire audio file
    try:
        text = recognizer.recognize_google(audio)
        print("Transcription: " + text)
        
        # Save the transcription to the memory file
        save_transcription(text)
        
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    filename = 'output.wav'  # This should match the filename from audio_record.py
    transcribe_audio(filename)  # Call the function if this file is run directly
