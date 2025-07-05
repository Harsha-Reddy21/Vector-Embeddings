import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Tabs, Tab } from '@mui/material';
import TicketForm from '../components/TicketForm';
import TicketList from '../components/TicketList';
import { getTickets } from '../services/api';

const HomePage = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const data = await getTickets();
      setTickets(data);
      setError(null);
    } catch (err) {
      setError('Failed to load tickets');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleTicketSubmitted = (result) => {
    // Add the new ticket to the list
    setTickets((prevTickets) => [result.ticket, ...prevTickets]);
  };

  // Filter tickets based on active tab
  const filteredTickets = tickets.filter(ticket => {
    if (activeTab === 0) return true; // All tickets
    if (activeTab === 1) return ticket.status === 'pending';
    if (activeTab === 2) return ticket.status === 'auto_resolved';
    if (activeTab === 3) return ticket.status === 'escalated';
    if (activeTab === 4) return ticket.status === 'resolved';
    return true;
  });

  return (
    <Container maxWidth="lg">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Customer Support System
        </Typography>
        
        <TicketForm onTicketSubmitted={handleTicketSubmitted} />
        
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={activeTab} onChange={handleTabChange} aria-label="ticket filter tabs">
            <Tab label="All Tickets" />
            <Tab label="Pending" />
            <Tab label="Auto-Resolved" />
            <Tab label="Escalated" />
            <Tab label="Resolved" />
          </Tabs>
        </Box>
        
        <TicketList 
          tickets={filteredTickets} 
          loading={loading} 
          error={error} 
        />
      </Box>
    </Container>
  );
};

export default HomePage; 