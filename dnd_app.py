import tkinter as tk
from PIL import Image, ImageTk
from audio.audio_record import AudioRecorder
from audio.transcribe_audio import transcribe_audio
from audio.analyze_text_for_image import analyze_text_for_image
from image.generate_image_flux import generate_image_flux
import threading
import time
import os
from audio.memory_manager import MemoryManager
import logging

# Set up logging to file and console
logging.basicConfig(
    filename="dnd_text_log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)
logging.getLogger().handlers[0].flush()

class DNDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DND AI Art Companion")
        self.root.geometry("800x600")

        # Set up memory manager and recorder
        self.memory_manager = MemoryManager()
        self.recorder = AudioRecorder(recording_callback=self.update_recording_indicator)
        self.recording = False
        self.lock = threading.Lock()
        self.current_image = None

        # Set up GUI elements
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Character description input and upload button
        tk.Label(self.root, text="Enter Character Description:").place(relx=0.05, rely=0.75)
        self.character_entry = tk.Entry(self.root, width=50)
        self.character_entry.place(relx=0.05, rely=0.78)

        self.upload_button = tk.Button(self.root, text="Upload Character", command=self.upload_character)
        self.upload_button.place(relx=0.05, rely=0.85)

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(relx=0.05, rely=0.88)

        self.record_button = tk.Button(self.root, text="Start Recording", command=self.toggle_recording)
        self.record_button.place(relx=0.05, rely=0.9)

        self.recording_indicator = tk.Label(self.root, text="Mic is off", bg="black", fg="white", relief=tk.RAISED)
        self.recording_indicator.place(relx=0.85, rely=0.1, width=120, height=50)

    def upload_character(self):
        character_description = self.character_entry.get()
        if character_description:
            self.memory_manager.update_memory("characters", "Character", character_description)
            logging.info("Character saved to memory.")
            self.status_label.config(text="Character saved to memory.")
            self.character_entry.delete(0, tk.END)
            self.root.after(2000, lambda: self.status_label.config(text=""))

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.record_button.config(text="Stop Recording")
        self.recorder.start_recording()
        self.update_recording_indicator(True)
        threading.Thread(target=self.capture_audio_chunks, daemon=True).start()
        threading.Thread(target=self.process_audio, daemon=True).start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="Start Recording")
        self.update_recording_indicator(False)
        with self.lock:
            filename = f"recording_{int(time.time())}.wav"
            success = self.recorder.stop_recording(filename)
            if success:
                logging.info(f"Final audio saved: {filename}")

    def capture_audio_chunks(self):
        while self.recording:
            with self.lock:
                self.recorder.record_chunk()
            time.sleep(0.1)

    def process_audio(self):
        while self.recording:
            time.sleep(10)
            filename = f"segment_{int(time.time())}.wav"

            with self.lock:
                logging.info("Processing audio...")
                success = self.recorder.stop_recording(filename)

                if success and os.path.exists(filename) and os.path.getsize(filename) > 0:
                    logging.info("Transcribing audio...")
                    text = transcribe_audio(filename)
                    if text:
                        logging.info("Analyzing text for image...")
                        prompt = analyze_text_for_image(text, self.memory_manager)
                        if prompt != "none":
                            self.display_image(prompt)
                self.recorder.start_recording()

    def display_image(self, prompt):
        image_path = generate_image_flux(prompt)
        
        if image_path:
            img = Image.open(image_path)
            img = img.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.current_image = img_tk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
            self.record_button.lift()

    def update_recording_indicator(self, is_recording):
        if is_recording:
            self.recording_indicator.config(bg="red", text="Mic is live")
        else:
            self.recording_indicator.config(bg="black", text="Mic is off")

# Initialize Tkinter and start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DNDApp(root)
    root.mainloop()
