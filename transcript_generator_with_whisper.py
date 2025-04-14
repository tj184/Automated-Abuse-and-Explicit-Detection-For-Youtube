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
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_file = f"{base_name}_temp_audio.wav"
    transcript_file = f"{base_name}_transcript.txt"
    extract_audio_ffmpeg(video_path, audio_file)
    transcription = transcribe_audio(audio_file, language=language)
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    if os.path.exists(audio_file):
        os.remove(audio_file)
    print(f" Transcript saved to {transcript_file}")
    return transcript_file
