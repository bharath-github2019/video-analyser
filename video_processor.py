import cv2
import os
import base64


class VideoProcessor:
    def __init__(self):
        os.makedirs("frames", exist_ok=True)

    def extract_frames(self, video_path, num_frames=10):
        """Extract evenly-spaced frames from a video and return as base64."""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            cap.release()
            raise RuntimeError("Video has no frames")

        step = max(1, total_frames // num_frames)
        frame_indices = [i * step for i in range(num_frames)]

        frames_b64 = []
        for idx, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                continue

            # Resize to save tokens (max 800px wide)
            h, w = frame.shape[:2]
            if w > 800:
                scale = 800 / w
                frame = cv2.resize(frame, (800, int(h * scale)))

            # Save preview
            path = f"frames/frame_{idx}.jpg"
            cv2.imwrite(path, frame)

            # Encode to base64
            _, buffer = cv2.imencode(".jpg", frame)
            frames_b64.append(base64.b64encode(buffer).decode())

        cap.release()
        return frames_b64

    def get_info(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total / fps if fps > 0 else 0
        cap.release()
        return {
            "duration": round(duration, 1),
            "fps": round(fps, 1),
            "frames": total
        }
