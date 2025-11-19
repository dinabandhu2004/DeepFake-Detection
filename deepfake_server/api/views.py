from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import tempfile
from tensorflow.keras.models import load_model
from .utils import extract_frames

# Load deepfake classifier once at startup
model = load_model("api/deepfake.h5")

# ----------------------------
# Health endpoint (prevents Render cold start)
# ----------------------------
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

# ----------------------------
# Video prediction endpoint
# ----------------------------
@api_view(['POST'])
def predict_video(request):
    # Force CORS headers for safety
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }

    video_file = request.FILES.get('video')
    if not video_file:
        return Response({"status": "fail", "message": "No video file provided"}, status=400, headers=headers)

    filename = video_file.name
    video_bytes = video_file.read()
    video_file.seek(0)

    try:
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=True) as temp_video:
            temp_video.write(video_bytes)
            temp_video.flush()

            # Extract frames
            frames = extract_frames(temp_video.name, frame_count=20)

        if len(frames) == 0:
            return Response({"status": "fail", "message": "No frames extracted"}, status=400, headers=headers)

        # Make predictions
        predictions = model.predict(frames)  # frames shape: (20, 126, 126, 3)
        avg_pred = np.mean(predictions, axis=0)
        real_acc = float(avg_pred[0])
        fake_acc = float(avg_pred[1])
        prediction = "REAL" if real_acc > fake_acc else "FAKE"

        return Response({
            "status": "success",
            "filename": filename,
            "prediction": prediction,
            "real_accuracy": round(real_acc, 4),
            "fake_accuracy": round(fake_acc, 4)
        }, headers=headers)

    except Exception as e:
        return Response({"status": "fail", "message": str(e)}, status=500, headers=headers)
