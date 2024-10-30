from audio_record import AudioRecorder
import time

def test_audio_recorder():
    recorder = AudioRecorder()
    recorder.start_recording()
    
    # Record for a specific duration
    duration = 5  # seconds
    print(f"Recording for {duration} seconds...")

    # Continuously record audio chunks
    start_time = time.time()
    while time.time() - start_time < duration:
        recorder.record_chunk()  # Record a chunk of audio
        time.sleep(0.1)  # Short delay to prevent CPU overload

    print("Stopping recording...")
    # Save recording
    recorder.stop_recording("test_output.wav")
    recorder.close()
    print("Recording saved as test_output.wav")

if __name__ == "__main__":
    test_audio_recorder()
