import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import TicketDetail from '../components/TicketDetail';
import { getTicketDetails } from '../services/api';

const TicketDetailPage = () => {
  const { ticketId } = useParams();
  const navigate = useNavigate();
  const [ticketData, setTicketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTicketDetails = async () => {
    setLoading(true);
    try {
      const data = await getTicketDetails(ticketId);
      setTicketData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load ticket details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (ticketId) {
      fetchTicketDetails();
    }
  }, [ticketId]);

  const handleResponseAdded = () => {
    // Refresh ticket details after adding a response
    fetchTicketDetails();
  };

  return (
    <Container maxWidth="lg">
      <Box my={4}>
        <Box display="flex" alignItems="center" mb={3}>
          <Button 
            startIcon={<ArrowBackIcon />} 
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            Back to Tickets
          </Button>
          <Typography variant="h4" component="h1">
            Ticket #{ticketId?.substring(0, 8)}
          </Typography>
        </Box>
        
        <TicketDetail 
          ticket={ticketData?.ticket}
          responses={ticketData?.responses}
          loading={loading}
          error={error}
          onResponseAdded={handleResponseAdded}
        />
      </Box>
    </Container>
  );
};

export default TicketDetailPage; 