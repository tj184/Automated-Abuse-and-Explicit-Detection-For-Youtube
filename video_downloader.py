import yt_dlp
import os

def download_video(url):
    try:
        video_path = None
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'vid_down.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f" Downloading: {url}")
            info_dict = ydl.extract_info(url, download=True)
            video_ext = info_dict.get("ext", "mp4")
            video_path = os.path.abspath(f"vid_down.{video_ext}")
        
        print(f" Download complete: {video_path}")
        return video_path

    except Exception as e:
        print(f" Error downloading video: {e}")
        return None
