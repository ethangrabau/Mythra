from audio.audio_record import record_audio
from audio.transcribe_audio import transcribe_audio
from audio.analyze_text_for_image import analyze_text_for_image  # Updated to reflect new function
from image.generate_image_flux import generate_image_flux  # Import your Flux image generation function


if __name__ == "__main__":
    filename = "output.wav"  # Use the same filename as in audio_record.py
    record_audio(filename)  # Record the audio and save it
    text = transcribe_audio(filename)  # Transcribe the audio file

    if text:  # Check if transcription was successful
        decision = analyze_text_for_image(text)  # Get AI decision whether to generate an image
        
        if decision and decision.lower() != "none":  # Check if AI decided to generate an image
            print("Generating image based on prompt: " + decision)
            generate_image_flux(decision)  # Call the Flux image generation function with the AI's prompt
        else:
            print("No image will be generated for this segment.")
