import React, { useState, useRef } from "react";
import axios from "axios";

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
    <div style={{ maxWidth: "600px", margin: "50px auto", textAlign: "center" }}>
      <h2>Deepfake Detection</h2>
      
      {/* Video Player */}
      {videoUrl && (
        <div style={{ marginBottom: "20px" }}>
          <video
            ref={videoRef}
            src={videoUrl}
            controls
            autoPlay
            muted
            style={{
              maxWidth: "100%",
              maxHeight: "300px",
              border: "1px solid #ddd",
              borderRadius: "8px"
            }}
            onPlay={() => console.log("Video started playing")}
          >
            Your browser does not support the video tag.
          </video>
        </div>
      )}
      
      <input 
        type="file" 
        accept="video/*" 
        onChange={handleFileChange} 
        style={{ marginBottom: "10px" }}
      />
      <br />
      <button
        onClick={handleUpload}
        style={{ 
          marginTop: "10px", 
          padding: "10px 20px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer"
        }}
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Detect"}
      </button>

      {result && (
        <div style={{ 
          marginTop: "20px", 
          textAlign: "left",
          padding: "15px",
          backgroundColor: "#f8f9fa",
          borderRadius: "8px",
          border: "1px solid #dee2e6"
        }}>
          {result.status === "success" ? (
            <>
              <p><strong>Filename:</strong> {result.filename}</p>
              <p><strong>Prediction:</strong> {result.prediction}</p>
              <p><strong>Real Accuracy:</strong> {result.real_accuracy}</p>
              <p><strong>Fake Accuracy:</strong> {result.fake_accuracy}</p>
            </>
          ) : (
            <p style={{ color: "red" }}>{result.message}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default VideoUpload;