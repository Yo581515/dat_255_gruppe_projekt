import time

import numpy as np
import pyaudio
import librosa
import whisper
from open_ai_assistant import Assistant
import pyttsx3

engine = pyttsx3.init()


def live_recording(threshold=0.001, silence_wait_time=30):
    model = whisper.load_model("base")
    my_assistant = Assistant()

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAIT_FRAMES = silence_wait_time

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    recording = False
    frames_since_sound = 0
    continue_listening = True
    try:
        print("Hello! I'm listening. Speak to me.")
        while continue_listening:
            data = stream.read(CHUNK, exception_on_overflow=False)
            np_data = np.frombuffer(data, dtype=np.int16).astype(
                np.float32) / 32768.0  # Convert to NumPy array and normalize
            rms = librosa.feature.rms(y=np_data)[0, 0]  # Calculate RMS value
            print(int(rms * 100000))
            if rms > threshold:  # If sound detected
                recording = True
                frames_since_sound = 0
                frames.append(data)
            elif recording:

                frames_since_sound += 1
                frames.append(data)
                if frames_since_sound > WAIT_FRAMES:  # Wait for silence before processing
                    recording = False
                    print("Processing audio...")
                    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
                    result = model.transcribe(audio_data, language="en")
                    print("Transcription:", result['text'])
                    print("Message sent.")
                    response, continue_listening = my_assistant.send_message(result['text'])
                    print("continue_listening:", continue_listening)
                    print("Response:\n", response)
                    engine.say(response)
                    engine.runAndWait()
                    time.sleep(1)
                    frames = []  # Reset frames after processing
    except KeyboardInterrupt:
        my_assistant.dissconnect_assistant()
        print("\nExiting.")
    finally:
        my_assistant.dissconnect_assistant()
        stream.stop_stream()
        stream.close()
        p.terminate()


live_recording()
