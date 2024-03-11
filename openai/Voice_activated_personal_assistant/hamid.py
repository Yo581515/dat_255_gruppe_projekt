import numpy as np
import pyaudio
import audioop
import whisper


def live_recording(wait_time=30):
    model = whisper.load_model("base")

    global r
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    recorder = pyaudio.PyAudio()

    stream = recorder.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

    frames = []
    recording = False
    frames_recorded = 0

    try:
        while True:
            frames_recorded += 1
            data = stream.read(CHUNK)
            rms = audioop.rms(data, 2)

            print(rms)

            if rms > 300:
                recording = True
                frames_recorded = 0

                print("Recording...")

            elif recording and frames_recorded > wait_time:
                recording = False
                print("Recording stopped")

                audio_data = b''.join(frames)
                WAVE_OUTPUT_FILENAME = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                print("Transcribing...")

                result = model.transcribe(WAVE_OUTPUT_FILENAME, language="en")
                print("Transcription:", result['text'])
                frames = []



            if recording:
                frames.append(data)
                # sounddevice.RawStream

    except KeyboardInterrupt:
        pass

    # close the stream
    stream.stop_stream()
    stream.close()
    # close PyAudio
    recorder.terminate()


live_recording()
