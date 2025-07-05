import React, { useRef, useEffect } from 'react';

const VideoPlayer = ({ videoUrl, currentTime = 0, onTimeUpdate }) => {
  const videoRef = useRef(null);

  // Set the current time when it changes
  useEffect(() => {
    if (videoRef.current && currentTime > 0) {
      videoRef.current.currentTime = currentTime;
      videoRef.current.play().catch(error => {
        console.error('Error playing video:', error);
      });
    }
  }, [currentTime]);

  // Handle time updates
  const handleTimeUpdate = () => {
    if (videoRef.current && onTimeUpdate) {
      onTimeUpdate(videoRef.current.currentTime);
    }
  };

  return (
    <div className="video-container mb-4">
      <video
        ref={videoRef}
        controls
        width="100%"
        onTimeUpdate={handleTimeUpdate}
      >
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer; 