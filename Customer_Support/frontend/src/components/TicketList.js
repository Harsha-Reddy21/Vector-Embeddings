import React from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  List, 
  ListItem, 
  ListItemText, 
  Chip, 
  Divider,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

const TicketList = ({ tickets, loading, error }) => {
  const navigate = useNavigate();

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

  const handleTicketClick = (ticketId) => {
    navigate(`/tickets/${ticketId}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Paper elevation={3} sx={{ p: 3, mb: 4, bgcolor: '#fff4f4' }}>
        <Typography color="error">Error loading tickets: {error}</Typography>
      </Paper>
    );
  }

  if (!tickets || tickets.length === 0) {
    return (
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography>No tickets found.</Typography>
      </Paper>
    );
  }

  return (
    <Paper elevation={3} sx={{ mb: 4 }}>
      <List sx={{ width: '100%' }}>
        {tickets.map((ticket, index) => (
          <React.Fragment key={ticket.id}>
            <ListItem 
              alignItems="flex-start" 
              sx={{ 
                cursor: 'pointer',
                '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.04)' }
              }}
              onClick={() => handleTicketClick(ticket.id)}
            >
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="subtitle1" component="span">
                      {ticket.text.length > 60 
                        ? `${ticket.text.substring(0, 60)}...` 
                        : ticket.text}
                    </Typography>
                    <Chip 
                      label={ticket.category || 'Uncategorized'} 
                      size="small" 
                      color="primary" 
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <Box mt={1}>
                    <Box display="flex" justifyContent="space-between">
                      <Typography variant="body2" component="span" color="text.secondary">
                        Customer: {ticket.customer_id}
                      </Typography>
                      <Chip 
                        label={ticket.status} 
                        size="small" 
                        color={getStatusColor(ticket.status)}
                      />
                    </Box>
                    {ticket.submitted_at && (
                      <Typography variant="caption" display="block" color="text.secondary" mt={0.5}>
                        Submitted: {new Date(ticket.submitted_at).toLocaleString()}
                      </Typography>
                    )}
                  </Box>
                }
              />
            </ListItem>
            {index < tickets.length - 1 && <Divider component="li" />}
          </React.Fragment>
        ))}
      </List>
    </Paper>
  );
};

export default TicketList; 