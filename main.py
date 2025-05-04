from video_downloader import download_video
from transcript_generator import generate_transcript
from adult_content_detection import analyze_video
from detoxify_hatebert_report import analyze_text_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_pdf_report(file_path, transcript_path, text_analysis, video_analysis, output_pdf="video_analysis_report.pdf"):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    line_height = 20
    y = height - 40

    def write_line(text):
        nonlocal y
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(40, y, text)
        y -= line_height

    # Header
    write_line("VIDEO CONTENT ANALYSIS REPORT")
    write_line(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    write_line("-" * 90)

    # Section 1: Download & Transcript Info
    write_line(f"Video file path     : {file_path}")
    write_line(f"Transcript file path: {transcript_path}")
    write_line("-" * 90)

    # Section 2: Toxicity & Hate Speech
    write_line("TOXICITY & HATE SPEECH ANALYSIS")
    write_line("[Detoxify]")
    for label, score in text_analysis["detoxify"].items():
        write_line(f"  {label.capitalize():<15}: {score:.4f}")
    write_line("[HateBERT]")
    for label, prob in text_analysis["hatebert"].items():
        write_line(f"  {label.capitalize():<15}: {prob:.4f}")
    write_line("Final Verdict:")
    write_line(f"  {text_analysis['final_verdict']}")
    write_line("-" * 90)

    # Section 3: Adult Content Analysis
    write_line("ADULT CONTENT DETECTION")
    for key, value in video_analysis.items():
        write_line(f"{key.capitalize():<20}: {value}")
    write_line("-" * 90)

    c.save()
    print(f"[INFO] PDF report generated at: {output_pdf}")

# --- Main Logic ---

url = "https://youtu.be/TFnJFaWwlbs?si=D6ojkAcTSmR4h2Q7"
video_file_path = download_video(url)

if video_file_path:
    print("Video downloaded to:", video_file_path)
else:
    print("Download failed.")
    exit()

video_file_path = 'vid_down.webm'
transcript_path = generate_transcript(video_file_path)
text_analysis_english = analyze_text_file("vid_down_transcript.txt")
video_analysis_result = analyze_video(video_file_path)

# Create PDF report
create_pdf_report(video_file_path, transcript_path, text_analysis_english, video_analysis_result)
