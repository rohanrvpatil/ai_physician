from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

async def generate_speech(response_text):
    audio_output_path = "response_audio.wav"
    tts.tts_to_file(text=response_text, file_path=audio_output_path)
    return audio_output_path
