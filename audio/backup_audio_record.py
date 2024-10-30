import pyaudio
import wave
import time

# Set up parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8192  # Increased CHUNK size from 4096 to 8192

class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.stream = None
        self.audio = pyaudio.PyAudio()
        self.recording = False

    def start_recording(self):
        """Start recording audio in one continuous stream."""
        self.frames = []
        try:
            self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                          rate=RATE, input=True,
                                          frames_per_buffer=CHUNK)
            self.recording = True
            print("Recording started...")
        except OSError as e:
            print(f"Error starting recording: {e}")

    def record_chunk(self):
        """Record a chunk of audio and append it to the frames list."""
        if self.stream and self.recording:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.frames.append(data)
                print(f"Recorded chunk of size: {len(data)} bytes")  # Debugging log to ensure chunks are captured
            except OSError as e:
                print(f"Buffer overflow error: {e}. Retrying in 100ms...")
                time.sleep(0.1)

    def stop_recording(self, filename):
        """Stop the recording and save the audio to a file."""
        if self.stream:
            self.recording = False
            try:
                self.stream.stop_stream()
                self.stream.close()
                print("Recording stopped!")
            except OSError as e:
                print(f"Error stopping stream: {e}")

            # Check if any frames were captured before saving
            if not self.frames:
                print("No audio frames captured!")
                return False  # Indicate failure to capture audio

            # Save the recorded frames as a .wav file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(self.frames))

            print(f"Audio saved as {filename}")
            self.frames = []  # Clear frames for the next recording
            return True  # Indicate success
        return False  # If stream was not open, indicate failure

    def close(self):
        """Terminate the PyAudio session."""
        try:
            self.audio.terminate()
        except Exception as e:
            print(f"Error terminating PyAudio: {e}")
