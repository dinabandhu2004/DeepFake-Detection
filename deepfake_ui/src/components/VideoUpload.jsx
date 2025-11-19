import React, { useState, useRef } from "react";
import axios from "axios";
import './videoupload.css'

const VideoUpload = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const videoRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideoFile(file);
      setResult(null);

      // Create URL for the selected video file
      const url = URL.createObjectURL(file);
      setVideoUrl(url);
    }
  };

  const handleUpload = async () => {
    if (!videoFile) {
      alert("Please select a video file!");
      return;
    }

    const formData = new FormData();
    formData.append("video", videoFile);

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL_FIRSTENDPOINT}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          maxBodyLength: Infinity,
          maxContentLength: Infinity,
          timeout: 0,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      setResult({ status: "fail", message: "Error uploading video" });
    }

    setLoading(false);
  };

  // Auto-play video when videoUrl changes
  React.useEffect(() => {
    if (videoRef.current && videoUrl) {
      videoRef.current.play().catch(error => {
        console.log("Auto-play was prevented:", error);
        // Handle cases where auto-play might be blocked by browser
      });
    }
  }, [videoUrl]);

  // Clean up object URL when component unmounts
  React.useEffect(() => {
    return () => {
      if (videoUrl) {
        URL.revokeObjectURL(videoUrl);
      }
    };
  }, [videoUrl]);

  return (
    < div className="main">
      <h2 className="header">Deepfake Detection</h2>

      <div className="video-upload-wrapper">

        <div className="video-box">
          {videoUrl ? (
            <video
              ref={videoRef}
              src={videoUrl}
              controls
              autoPlay
              muted
            />
          ) : (
            "video will be played here"
          )}
        </div>

        <div className="upload-box">
          <p>upload video here</p>
          <input type="file" accept="video/*" onChange={handleFileChange} />
          <button className="upload-btn" onClick={handleUpload}>
            {loading ? "Processing..." : "Upload & Predict"}
          </button>
        </div>

      </div>

      <div className="result-container">
        {result && (
          <div>
            {result.status === "success" ? (
              <>
                <p><strong>Filename:</strong> {result.filename}</p>
                <p><strong>Prediction:</strong> {result.prediction}</p>
                <p><strong>Real Accuracy:</strong> {result.real_accuracy}</p>
                <p><strong>Fake Accuracy:</strong> {result.fake_accuracy}</p>
              </>
            ) : (
              <p>{result.message}</p>
            )}
          </div>
        )}
      </div>



    </div>
  );
};

export default VideoUpload;