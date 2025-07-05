import React, { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Paper, 
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import { submitTicket } from '../services/api';

const TicketForm = ({ onTicketSubmitted }) => {
  const [formData, setFormData] = useState({
    text: '',
    customer_id: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await submitTicket(formData);
      setSuccess(true);
      setFormData({
        text: '',
        customer_id: '',
      });
      if (onTicketSubmitted) {
        onTicketSubmitted(result);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit ticket');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Submit a Support Ticket
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          label="Customer ID"
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          margin="normal"
          required
          variant="outlined"
        />
        
        <TextField
          fullWidth
          label="How can we help you?"
          name="text"
          value={formData.text}
          onChange={handleChange}
          margin="normal"
          required
          multiline
          rows={4}
          variant="outlined"
          placeholder="Describe your issue in detail..."
        />
        
        <Button
          type="submit"
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Submit Ticket'}
        </Button>
      </Box>
      
      <Snackbar 
        open={success} 
        autoHideDuration={6000} 
        onClose={() => setSuccess(false)}
      >
        <Alert severity="success" onClose={() => setSuccess(false)}>
          Ticket submitted successfully!
        </Alert>
      </Snackbar>
      
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Paper>
  );
};

export default TicketForm; 