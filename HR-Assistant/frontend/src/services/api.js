import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Document Management
export const uploadDocuments = async (files, documentType, category) => {
  const formData = new FormData();
  
  files.forEach((file) => {
    formData.append('files', file);
  });
  
  formData.append('document_type', documentType);
  formData.append('category', category);
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/documents');
  return response.data.documents;
};

export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/documents/${documentId}`);
  return response.data;
};

// Categories
export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data.categories;
};

// Query
export const queryAssistant = async (query, categories = null) => {
  const response = await api.post('/query', {
    query,
    categories,
  });
  
  return response.data;
};

export default api; 