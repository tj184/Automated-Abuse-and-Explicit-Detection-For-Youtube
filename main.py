
from video_downloader import download_video
from transcript_generator_with_whisper import generate_transcript
from explicit_content_detection import analyze_video

url = "Paste the yt link"
video_file_path = download_video(url)


if video_file_path:
    print("Video downloaded to:", video_file_path)
else:
    print("Download failed.")


video_file_path='vid_down.webm'

transcript_path = generate_transcript(video_file_path)

print("Transcript file is located at:", transcript_path)



result = analyze_video(video_file_path)

print(result["output"])
