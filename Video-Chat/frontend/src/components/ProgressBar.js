import React from 'react';

const ProgressBar = ({ progress, status }) => {
  // Convert progress to percentage
  const percentage = Math.round(progress * 100);
  
  // Determine the color based on status
  let color = 'bg-primary';
  if (status === 'error') {
    color = 'bg-danger';
  } else if (status === 'completed') {
    color = 'bg-success';
  }

  // Get status text
  const getStatusText = () => {
    switch (status) {
      case 'queued':
        return 'Queued for processing';
      case 'extracting_audio':
        return 'Extracting audio from video';
      case 'transcribing':
        return 'Transcribing audio';
      case 'processing_text':
        return 'Processing transcript';
      case 'completed':
        return 'Processing completed';
      case 'error':
        return 'Error processing video';
      default:
        return 'Processing';
    }
  };

  return (
    <div className="progress-container">
      <div className="progress">
        <div
          className={`progress-bar ${color}`}
          role="progressbar"
          style={{ width: `${percentage}%` }}
          aria-valuenow={percentage}
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {percentage}%
        </div>
      </div>
      <div className="mt-2 text-center">
        <strong>Status:</strong> {getStatusText()}
      </div>
    </div>
  );
};

export default ProgressBar; 