import tkinter as tk
from PIL import Image, ImageTk
from audio.audio_record import AudioRecorder
from audio.transcribe_audio import transcribe_audio
from audio.analyze_text_for_image import analyze_text_for_image
from image.generate_image_flux import generate_image_flux
import threading
import time
import os

class DNDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DND AI Art Companion")
        self.root.geometry("800x600")  # Half-screen size

        # Set up UI elements
        self.canvas = tk.Canvas(self.root, bg='black')  # Background for images
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Record button, positioned on top of the image
        self.record_button = tk.Button(self.root, text="Start Recording", command=self.toggle_recording)
        self.record_button.place(relx=0.05, rely=0.9)  # Position at bottom-left corner

        # App state
        self.recording = False
        self.recorder = AudioRecorder()  # Instantiate the recorder
        self.lock = threading.Lock()  # Thread lock to prevent conflicts

        # Placeholder for the image object to prevent garbage collection
        self.current_image = None

    def toggle_recording(self):
        """Toggle recording on or off."""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start audio recording and process audio chunks every 10 seconds."""
        self.recording = True
        self.record_button.config(text="Stop Recording")
        self.recorder.start_recording()  # Start recording audio
        threading.Thread(target=self.capture_audio_chunks, daemon=True).start()  # Capture chunks in background
        threading.Thread(target=self.process_audio, daemon=True).start()  # Start the audio processing thread

    def stop_recording(self):
        """Stop recording and finalize the audio."""
        self.recording = False
        self.record_button.config(text="Start Recording")
        with self.lock:  # Ensure recording stops cleanly
            filename = f"recording_{int(time.time())}.wav"  # Example: timestamped filename
            success = self.recorder.stop_recording(filename)  # Stop recording and save the file
            self.recorder.close()  # Close the recorder
            if success:
                print(f"Final audio saved: {filename}")
            else:
                print("No audio frames captured; nothing was saved.")

    def capture_audio_chunks(self):
        """Capture audio in chunks while recording is active."""
        while self.recording:
            with self.lock:  # Ensure safe recording
                self.recorder.record_chunk()  # Record chunks continuously
            time.sleep(0.1)  # Sleep for a short interval to avoid CPU overload

    def process_audio(self):
        """Process audio every 10 seconds if recording is active."""
        while self.recording:
            time.sleep(10)  # Wait for 10 seconds
            filename = f"segment_{int(time.time())}.wav"  # Example: timestamped filename
            
            with self.lock:  # Ensure audio is processed without recording conflicts
                print("Processing audio...")
                success = self.recorder.stop_recording(filename)  # Stop recording to save current audio

                if success and os.path.exists(filename) and os.path.getsize(filename) > 0:
                    print("Transcribing audio...")
                    text = transcribe_audio(filename)
                    if text:
                        print("Analyzing text for image...")
                        prompt = analyze_text_for_image(text)
                        if prompt != "none":
                            self.display_image(prompt)
                else:
                    print(f"Audio file {filename} is empty or does not exist.")

                # Restart recording for the next 10 seconds
                self.recorder.start_recording()

    def display_image(self, prompt):
        """Generate and display an image based on the given prompt."""
        image_path = generate_image_flux(prompt)  # Get the path to the saved generated image
        
        if image_path:  # Check if an image was generated successfully
            img = Image.open(image_path)
            img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)  # Resize image
            img_tk = ImageTk.PhotoImage(img)

            # Clear previous images
            self.canvas.delete("all")

            # Store a reference to avoid garbage collection
            self.current_image = img_tk

            # Display the new image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)

            # Bring the record button back on top of the image
            self.record_button.lift()

# Initialize Tkinter and start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DNDApp(root)
    root.mainloop()
