import os
import whisper
import subprocess

def extract_audio_ffmpeg(video_path, audio_path):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio(audio_path, language=None):
    model = whisper.load_model("medium")
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def generate_transcript(video_path, language=None):
    # Derive file names from the video name
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_file = f"{base_name}_temp_audio.wav"
    transcript_file = f"{base_name}_transcript.txt"

    # Step 1: Extract audio from video
    extract_audio_ffmpeg(video_path, audio_file)

    # Step 2: Transcribe audio
    transcription = transcribe_audio(audio_file, language=language)

    # Step 3: Save transcript
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcription)

    # Optional: Clean up temp audio
    if os.path.exists(audio_file):
        os.remove(audio_file)

    print(f" Transcript saved to {transcript_file}")
    return transcript_file
