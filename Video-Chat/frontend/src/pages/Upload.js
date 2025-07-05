import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadVideo, getVideoStatus } from '../utils/api';
import ProgressBar from '../components/ProgressBar';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [videoId, setVideoId] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  const [processingProgress, setProcessingProgress] = useState(0);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  
  // Poll for processing status if videoId exists
  useEffect(() => {
    let interval;
    
    if (videoId) {
      interval = setInterval(async () => {
        try {
          const status = await getVideoStatus(videoId);
          setProcessingStatus(status.status);
          setProcessingProgress(status.progress || 0);
          
          // If processing is complete or error, clear interval
          if (status.status === 'completed' || status.status === 'error') {
            clearInterval(interval);
            
            // If completed, redirect to chat page after a delay
            if (status.status === 'completed') {
              setTimeout(() => {
                navigate(`/chat/${videoId}`);
              }, 2000);
            }
          }
        } catch (err) {
          console.error('Error checking processing status:', err);
          clearInterval(interval);
        }
      }, 3000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [videoId, navigate]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      setUploadError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadError('Please select a file to upload');
      return;
    }

    try {
      setUploading(true);
      setUploadError(null);
      
      const response = await uploadVideo(file);
      setVideoId(response.video_id);
      setProcessingStatus('queued');
      setProcessingProgress(0);
    } catch (err) {
      console.error('Error uploading video:', err);
      setUploadError('Failed to upload video. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1 className="mb-4">Upload Lecture Video</h1>
      
      {!videoId ? (
        <div className="card">
          <div className="card-body">
            <div
              className="upload-container"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="video/*"
                style={{ display: 'none' }}
              />
              <h3>Drag & Drop or Click to Upload</h3>
              <p>Supported formats: MP4, AVI, MOV, MKV</p>
              {file && <p className="mt-3">Selected: {file.name}</p>}
            </div>

            {uploadError && (
              <div className="alert alert-danger mt-3" role="alert">
                {uploadError}
              </div>
            )}

            <div className="d-grid gap-2 mt-4">
              <button
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={!file || uploading}
              >
                {uploading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Uploading...
                  </>
                ) : (
                  'Upload Video'
                )}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="card">
          <div className="card-body">
            <h3 className="mb-3">Processing Video</h3>
            <p>Your video is being processed. This may take a while depending on the length of the video.</p>
            <ProgressBar progress={processingProgress} status={processingStatus} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload; 