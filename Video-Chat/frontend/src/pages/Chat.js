import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getVideoMetadata, sendChatMessage } from '../utils/api';
import VideoPlayer from '../components/VideoPlayer';
import ChatMessage from '../components/ChatMessage';

const Chat = () => {
  const { videoId } = useParams();
  const navigate = useNavigate();
  const [videoMetadata, setVideoMetadata] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const chatContainerRef = useRef(null);
  
  // Base URL for video streaming
  const videoUrl = `/api/v1/videos/${videoId}/stream`;

  // Fetch video metadata when component mounts
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const data = await getVideoMetadata(videoId);
        setVideoMetadata(data);
        
        // Redirect if video is not processed
        if (!data.transcript_available) {
          navigate('/');
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching video metadata:', err);
        setError('Failed to load video information. Please try again later.');
        setLoading(false);
      }
    };

    fetchMetadata();
  }, [videoId, navigate]);
  
  // Scroll to bottom of chat when messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim()) return;
    
    try {
      setSending(true);
      
      // Add user message to chat
      const userMessage = { role: 'user', content: newMessage };
      setMessages((prev) => [...prev, userMessage]);
      setNewMessage('');
      
      // Send message to API
      const response = await sendChatMessage(videoId, newMessage);
      
      // Add assistant response to chat
      const assistantMessage = { 
        role: 'assistant', 
        content: response.message,
        timestamps: response.timestamps 
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setSending(false);
    }
  };

  const handleTimestampClick = (time) => {
    setCurrentTime(time);
  };

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
      <h1 className="mb-4">Chat with Lecture</h1>
      
      <div className="row">
        <div className="col-lg-6 mb-4">
          <VideoPlayer 
            videoUrl={videoUrl} 
            currentTime={currentTime}
            onTimeUpdate={setCurrentTime}
          />
          
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">{videoMetadata.filename}</h5>
              <p className="card-text">
                <small className="text-muted">
                  Uploaded: {new Date(videoMetadata.upload_time).toLocaleString()}
                </small>
              </p>
            </div>
          </div>
        </div>
        
        <div className="col-lg-6">
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Ask Questions About the Lecture</h5>
            </div>
            <div className="card-body">
              <div 
                className="chat-container mb-3 p-3 border rounded"
                ref={chatContainerRef}
              >
                {messages.length === 0 ? (
                  <div className="text-center text-muted my-5">
                    <p>Ask a question about the lecture content!</p>
                    <p>Example: "What are the key points discussed in this lecture?"</p>
                  </div>
                ) : (
                  messages.map((msg, index) => (
                    <ChatMessage
                      key={index}
                      message={msg.content}
                      role={msg.role}
                      timestamps={msg.timestamps}
                      onTimestampClick={handleTimestampClick}
                    />
                  ))
                )}
                
                {sending && (
                  <div className="text-center my-2">
                    <div className="spinner-grow spinner-grow-sm text-primary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  </div>
                )}
              </div>
              
              <form onSubmit={handleSendMessage}>
                <div className="input-group">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Type your question..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    disabled={sending}
                  />
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={!newMessage.trim() || sending}
                  >
                    Send
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat; 