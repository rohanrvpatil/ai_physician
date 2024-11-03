import asyncio

async def main_pipeline(audio_stream, face_video):
    async for audio_chunk in audio_stream:
        transcribed_text = await transcribe_audio(audio_chunk)
        print("User said:", transcribed_text)

        response_text = await generate_response(transcribed_text)
        print("Avatar response:", response_text)

        response_audio = await generate_speech(response_text)
        print("Generated speech audio:", response_audio)

        output_video = await lip_sync_video(face_video, response_audio)
        print("Lip-synced video output:", output_video)