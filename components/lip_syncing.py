import subprocess

async def lip_sync_video(face_video_path, audio_path, output_video_path="output_lip_synced.mp4"):
    command = [
        "python", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip.pth",
        "--face", face_video_path,
        "--audio", audio_path,
        "--outfile", output_video_path
    ]
    subprocess.run(command)
    return output_video_path
