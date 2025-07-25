🚀 Features
This project brings together multiple AI and automation tools to analyze YouTube videos for content and safety. Here's what it offers:

🎥 1. YouTube Video Downloading
Downloads videos directly from YouTube using the efficient and customizable yt_dlp library.

Supports downloading the best available quality by merging the best video and audio streams.

🔊 2. Audio Extraction from Video
Utilizes ffmpeg to extract clean, mono-channel, 16kHz audio in WAV format.

Ensures optimal audio quality for better transcription accuracy.

🧠 3. Speech-to-Text Transcription with Whisper
Employs OpenAI's Whisper, a powerful speech recognition model.

Transcribes the extracted audio into readable text.

Supports multilingual audio—transcribe videos in multiple languages by specifying the language code (e.g., "en", "hi").

📝 4. Transcript Export
Saves the final transcribed text in a .txt file for further analysis, record keeping, or integration into other workflows.

🛡️ 5. Abusive Language Detection (Planned/Optional Integration)
Implements a Multi-Level AI approach to analyze the transcript text.

Detects profanity, hate speech, or other forms of verbal abuse within the transcript.

Enhances the safety evaluation of online video content.

🔍 6. Explicit Content Detection in Video Frames
Analyzes individual frames of the video for any explicit, nudity, or adult content.

Can be integrated with image classifiers or pre-trained deep learning models.

Designed for moderation of unsafe or NSFW content in visual media.

📂 Dataset Reference for Explicit Content Detection:


*** Note-I have trained the model with  a small data size due to hardware limitation , perforamce can be improved with large dataset.***



############ Running the project ##########

Provide link of video in main.py and run the code. 


