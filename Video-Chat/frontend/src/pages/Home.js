import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getAllVideos } from '../utils/api';

const Home = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch all videos when component mounts
  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const data = await getAllVideos();
        setVideos(data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching videos:', err);
        setError('Failed to load videos. Please try again later.');
        setLoading(false);
      }
    };

    fetchVideos();
  }, []);

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Your Lecture Videos</h1>
        <Link to="/upload" className="btn btn-primary">
          Upload New Lecture
        </Link>
      </div>

      {videos.length === 0 ? (
        <div className="text-center my-5">
          <h3>No videos uploaded yet</h3>
          <p>Upload your first lecture video to get started!</p>
          <Link to="/upload" className="btn btn-lg btn-primary mt-3">
            Upload Lecture
          </Link>
        </div>
      ) : (
        <div className="row">
          {videos.map((video) => (
            <div key={video.video_id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{video.filename}</h5>
                  <p className="card-text">
                    <small className="text-muted">
                      Uploaded: {new Date(video.upload_time).toLocaleString()}
                    </small>
                  </p>
                  <p className="card-text">
                    Status:{' '}
                    <span className={video.status === 'processed' ? 'text-success' : 'text-warning'}>
                      {video.status === 'processed' ? 'Ready' : 'Processing'}
                    </span>
                  </p>
                </div>
                <div className="card-footer">
                  {video.transcript_available ? (
                    <Link
                      to={`/chat/${video.video_id}`}
                      className="btn btn-primary w-100"
                    >
                      Chat with Lecture
                    </Link>
                  ) : (
                    <button className="btn btn-secondary w-100" disabled>
                      Processing...
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home; 