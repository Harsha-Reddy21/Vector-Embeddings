import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Ticket API
export const submitTicket = async (ticketData) => {
  try {
    const response = await api.post('/tickets/', ticketData);
    return response.data;
  } catch (error) {
    console.error('Error submitting ticket:', error);
    throw error;
  }
};

export const getTickets = async () => {
  try {
    const response = await api.get('/tickets/');
    return response.data;
  } catch (error) {
    console.error('Error fetching tickets:', error);
    throw error;
  }
};

export const getTicketDetails = async (ticketId) => {
  try {
    const response = await api.get(`/tickets/${ticketId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching ticket ${ticketId}:`, error);
    throw error;
  }
};

export const addManualResponse = async (ticketId, responseText) => {
  try {
    const response = await api.post(`/tickets/${ticketId}/respond`, {
      response: responseText,
    });
    return response.data;
  } catch (error) {
    console.error('Error adding manual response:', error);
    throw error;
  }
};

// Knowledge Base API
export const getHistoricalTickets = async () => {
  try {
    const response = await api.get('/knowledge/historical-tickets');
    return response.data;
  } catch (error) {
    console.error('Error fetching historical tickets:', error);
    throw error;
  }
};

export const getCompanyDocs = async () => {
  try {
    const response = await api.get('/knowledge/company-docs');
    return response.data;
  } catch (error) {
    console.error('Error fetching company docs:', error);
    throw error;
  }
};

export const addHistoricalTicket = async (ticketData) => {
  try {
    const response = await api.post('/knowledge/add-ticket', ticketData);
    return response.data;
  } catch (error) {
    console.error('Error adding historical ticket:', error);
    throw error;
  }
};

export const addCompanyDoc = async (docData) => {
  try {
    const response = await api.post('/knowledge/add-document', docData);
    return response.data;
  } catch (error) {
    console.error('Error adding company document:', error);
    throw error;
  }
}; 