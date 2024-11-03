import whisper
import sounddevice as sd
import numpy as np
import asyncio

model = whisper.load_model("tiny.en")

async def transcribe_audio(audio_chunk):
    # print("Processing...")
    audio = whisper.pad_or_trim(audio_chunk)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language="en", without_timestamps=True)
    result = whisper.decode(model, mel, options)
    # print("Finished processing.")
    return result.text

async def audio_stream_generator(chunk_duration=1, sample_rate=16000, device=None):
    buffer = []

    def audio_callback(indata, frames, time, status):
        buffer.append(indata.copy())

    with sd.InputStream(samplerate=sample_rate, channels=1, device=device, callback=audio_callback):
        while True:
            await asyncio.sleep(chunk_duration)
            if buffer:
                audio_data = np.concatenate(buffer, axis=0).flatten()
                buffer.clear()
                yield audio_data

def list_input_devices():
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    print("Available input devices:")
    for i in input_devices:
        print(f"{i}: {devices[i]['name']}")
    return input_devices

async def main():
    input_devices = list_input_devices()
    device_index = int(input("Enter the number of the input device you want to use: "))
    if device_index not in input_devices:
        print("Invalid device selected.")
        return
    print("Device selected. Please say something...")
    async for audio_chunk in audio_stream_generator(device=device_index):
        # print("Waiting for input...")
        text = await transcribe_audio(audio_chunk)
        print("Detected text:", text)

asyncio.run(main())
