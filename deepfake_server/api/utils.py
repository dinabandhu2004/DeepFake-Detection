import cv2
import numpy as np

def extract_frames(video_path, frame_count=20):
    frames = []
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize to your model's input
        frame = cv2.resize(frame, (126, 126))

        # Normalize
        frame = frame / 255.0  

        frames.append(frame)

        if len(frames) == frame_count:
            break

    cap.release()
    return np.array(frames)
