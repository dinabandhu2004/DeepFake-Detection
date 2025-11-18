from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import tempfile
from tensorflow.keras.models import load_model

from .utils import extract_frames

# Load deepfake classifier
model = load_model("api/deepfake.h5")

# Load VGG16 feature extractor

@api_view(['POST'])
def predict_video(request):
    video_file = request.FILES.get('video')
    
    if not video_file:
        return Response({"status": "fail", "message": "No video file provided"}, status=400)

    filename = video_file.name
    video_bytes = video_file.read()
    video_file.seek(0)

    try:
        with tempfile.NamedTemporaryFile(delete=True) as temp_video:
            temp_video.write(video_bytes)
            temp_video.flush()

            # Extract frames
            frames = extract_frames(temp_video.name, frame_count=20)

        if len(frames) == 0:
            return Response({"status": "fail", "message": "No frames extracted"}, status=400)

        # Predict directly on frames
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
        })

    except Exception as e:
        return Response({"status": "fail", "message": str(e)}, status=500)
