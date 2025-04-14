import cv2
import os
import numpy as np
import tempfile
import subprocess
import io
from contextlib import redirect_stdout
from nudenet import NudeDetector
from tensorflow.keras.models import load_model

# Load your custom model
cnn_model = load_model('explicit_detection_model.h5')
detector = NudeDetector()

def convert_webm_to_mp4(input_path):
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "converted.mp4")
    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except subprocess.CalledProcessError:
        raise RuntimeError("FFmpeg failed to convert the video.")

def extract_frames(video_path, interval_sec=1):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or np.isnan(fps):
        raise ValueError("FPS is zero or undefined, possibly an unsupported codec or corrupt file.")

    interval = int(fps * interval_sec)
    frames = []
    i = 0
    success = True
    while success:
        success, frame = cap.read()
        if not success:
            break
        if i % interval == 0 and frame is not None:
            frames.append(frame)
        i += 1
    cap.release()
    return frames

def classify_frames(frames):
    results = []
    temp_dir = tempfile.mkdtemp()
    model_explicit_count = 0

    for idx, frame in enumerate(frames):
        filename = os.path.join(temp_dir, f"frame_{idx}.jpg")
        cv2.imwrite(filename, frame)

        resized_frame = cv2.resize(frame, (128, 128))
        scaled_frame = resized_frame.astype("float32") / 255.0
        input_frame = scaled_frame.reshape(1, 128, 128, 3)

        prediction = cnn_model.predict(input_frame, verbose=0)
        predicted_class = int(prediction[0][0] > 0.5)

        if predicted_class == 1:
            model_explicit_count += 1

        detections = detector.detect(filename)
        unsafe = any(det['class'] in ['EXPOSED_BREAST_F', 'EXPOSED_GENITALIA_F', 'EXPOSED_GENITALIA_M'] for det in detections)

        results.append({
            'filename': filename,
            'unsafe': unsafe,
            'detections': detections,
            'model_pred': predicted_class
        })

    print(f"\nFrames predicted as explicit by model: {model_explicit_count}/{len(frames)}")
    return results

def analyze_video(video_path):
    f = io.StringIO()
    with redirect_stdout(f):
        print("Extracting frames...")

        if video_path.endswith(".webm"):
            print("Detected .webm file, converting to .mp4 for processing...")
            video_path = convert_webm_to_mp4(video_path)

        frames = extract_frames(video_path)
        print(f"{len(frames)} frames extracted.")

        print("Classifying frames...")
        results = classify_frames(frames)

        unsafe_count = sum(1 for res in results if res['unsafe'])
        total_frames = len(results)
        unsafe_ratio = unsafe_count / total_frames if total_frames > 0 else 0

        if unsafe_ratio > 0.6:
            level = "High"
        elif unsafe_ratio > 0.3:
            level = "Moderate"
        elif unsafe_ratio > 0.1:
            level = "Low"
        else:
            level = "None"

        print("\n--- Analysis Report ---")
        print(f"Total Frames: {total_frames}")
        print(f"Unsafe Frames: {unsafe_count}")
        print(f"Unsafe Ratio: {unsafe_ratio:.2f}")
        print(f"NSFW Significance Level: {level}")

        unsafe_examples = [res for res in results if res['unsafe']]
        if level != "None":
            print("\nExamples of Unsafe Frames:")
            for example in unsafe_examples[:5]:
                print(f"- {os.path.basename(example['filename'])}: Detected {example['detections']}")

    return {
        "output": f.getvalue(),
        "total_frames": total_frames,
        "unsafe_frames": unsafe_count,
        "unsafe_ratio": unsafe_ratio,
        "significance_level": level,
        "examples": unsafe_examples[:5] if unsafe_count > 0 else []
    }
