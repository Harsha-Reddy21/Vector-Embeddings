import axios from 'axios';

const API_URL = '/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Video API
export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_URL}/videos/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getVideoStatus = async (videoId) => {
  const response = await api.get(`/videos/status/${videoId}`);
  return response.data;
};

export const getVideoMetadata = async (videoId) => {
  const response = await api.get(`/videos/${videoId}`);
  return response.data;
};

export const getAllVideos = async () => {
  const response = await api.get('/videos/');
  return response.data;
};

// Chat API
export const sendChatMessage = async (videoId, message) => {
  const response = await api.post('/chat', {
    video_id: videoId,
    message: message,
  });
  
  return response.data;
};

export default api; 