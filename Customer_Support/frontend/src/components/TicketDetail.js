import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Chip, 
  Divider, 
  TextField,
  Button,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Card,
  CardContent,
  Grid
} from '@mui/material';
import { addManualResponse } from '../services/api';

const TicketDetail = ({ ticket, responses, loading, error, onResponseAdded }) => {
  const [manualResponse, setManualResponse] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [responseError, setResponseError] = useState(null);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!ticket) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        No ticket selected
      </Alert>
    );
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'auto_resolved':
        return 'success';
      case 'escalated':
        return 'error';
      case 'pending':
        return 'warning';
      case 'resolved':
        return 'info';
      default:
        return 'default';
    }
  };

  const handleSubmitResponse = async () => {
    if (!manualResponse.trim()) return;
    
    setSubmitting(true);
    setResponseError(null);
    
    try {
      const result = await addManualResponse(ticket.id, manualResponse);
      setManualResponse('');
      if (onResponseAdded) {
        onResponseAdded(result);
      }
    } catch (err) {
      setResponseError(err.response?.data?.detail || 'Failed to submit response');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" component="h2">
            Ticket Details
          </Typography>
          <Chip 
            label={ticket.status} 
            color={getStatusColor(ticket.status)}
          />
        </Box>
        
        <Typography variant="body1" gutterBottom>
          {ticket.text}
        </Typography>
        
        <Box mt={2}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Customer ID: {ticket.customer_id}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Submitted: {new Date(ticket.submitted_at).toLocaleString()}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Category: {ticket.category || 'Uncategorized'}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                Confidence: {ticket.confidence ? `${(ticket.confidence * 100).toFixed(2)}%` : 'N/A'}
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </Paper>

      <Typography variant="h6" component="h3" gutterBottom>
        Responses
      </Typography>
      
      {responses && responses.length > 0 ? (
        <List>
          {responses.map((response, index) => (
            <Card key={response.id || index} sx={{ mb: 2 }}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="subtitle2" color="text.secondary">
                    {response.is_manual ? 'Manual Response' : 'AI Response'}
                  </Typography>
                  {response.created_at && (
                    <Typography variant="caption" color="text.secondary">
                      {new Date(response.created_at).toLocaleString()}
                    </Typography>
                  )}
                </Box>
                
                <Typography variant="body1" paragraph>
                  {response.response}
                </Typography>
                
                {response.sources && response.sources.length > 0 && (
                  <Box mt={2}>
                    <Typography variant="subtitle2">Sources:</Typography>
                    <List dense>
                      {response.sources.map((source, idx) => (
                        <ListItem key={idx} disablePadding>
                          <ListItemText 
                            primary={source.source} 
                            secondary={`From ${source.type}`} 
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
                
                {!response.is_manual && (
                  <Box display="flex" justifyContent="flex-end" mt={1}>
                    <Chip 
                      label={`Confidence: ${(response.confidence * 100).toFixed(2)}%`}
                      color={response.confidence > 0.75 ? "success" : "warning"}
                      size="small"
                    />
                  </Box>
                )}
              </CardContent>
            </Card>
          ))}
        </List>
      ) : (
        <Alert severity="info">No responses yet</Alert>
      )}
      
      <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" component="h3" gutterBottom>
          Add Manual Response
        </Typography>
        
        <TextField
          fullWidth
          label="Your response"
          value={manualResponse}
          onChange={(e) => setManualResponse(e.target.value)}
          margin="normal"
          required
          multiline
          rows={4}
          variant="outlined"
        />
        
        {responseError && (
          <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
            {responseError}
          </Alert>
        )}
        
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmitResponse}
          disabled={submitting || !manualResponse.trim()}
          sx={{ mt: 2 }}
        >
          {submitting ? <CircularProgress size={24} /> : 'Submit Response'}
        </Button>
      </Paper>
    </Box>
  );
};

export default TicketDetail; 