from audio.audio_record import record_audio
from audio.transcribe_audio import transcribe_audio
from audio.summarize_text import summarize_text
from image.generate_image_flux import generate_image_flux  # Import your Flux image generation function


if __name__ == "__main__":
    filename = "output.wav"  # Use the same filename as in audio_record.py
    record_audio(filename)  # Record the audio and save it
    text = transcribe_audio(filename)  # Transcribe the audio file
    if text:  # Check if transcription was successful
        summary = summarize_text(text)  # Summarize the transcribed text
        if summary:  # Check if summary is None or empty
            generate_image_flux(text)  # Call the Flux image generation function with the summary
