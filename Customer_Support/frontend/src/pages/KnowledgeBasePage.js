import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Tabs, 
  Tab, 
  Paper, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  ListItemText, 
  Divider,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import { 
  getHistoricalTickets, 
  getCompanyDocs, 
  addHistoricalTicket, 
  addCompanyDoc 
} from '../services/api';

const KnowledgeBasePage = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [historicalTickets, setHistoricalTickets] = useState([]);
  const [companyDocs, setCompanyDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  // Form states
  const [newTicket, setNewTicket] = useState({ text: '', solution: '' });
  const [newDoc, setNewDoc] = useState({ title: '', content: '' });
  const [submitting, setSubmitting] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ticketsData, docsData] = await Promise.all([
        getHistoricalTickets(),
        getCompanyDocs()
      ]);
      setHistoricalTickets(ticketsData);
      setCompanyDocs(docsData);
      setError(null);
    } catch (err) {
      setError('Failed to load knowledge base data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleTicketChange = (e) => {
    const { name, value } = e.target;
    setNewTicket(prev => ({ ...prev, [name]: value }));
  };

  const handleDocChange = (e) => {
    const { name, value } = e.target;
    setNewDoc(prev => ({ ...prev, [name]: value }));
  };

  const handleAddTicket = async (e) => {
    e.preventDefault();
    if (!newTicket.text.trim() || !newTicket.solution.trim()) return;
    
    setSubmitting(true);
    try {
      await addHistoricalTicket(newTicket);
      setNewTicket({ text: '', solution: '' });
      setSuccessMessage('Historical ticket added successfully');
      setSuccess(true);
      // Refresh data
      fetchData();
    } catch (err) {
      setError('Failed to add historical ticket');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleAddDoc = async (e) => {
    e.preventDefault();
    if (!newDoc.title.trim() || !newDoc.content.trim()) return;
    
    setSubmitting(true);
    try {
      await addCompanyDoc(newDoc);
      setNewDoc({ title: '', content: '' });
      setSuccessMessage('Company document added successfully');
      setSuccess(true);
      // Refresh data
      fetchData();
    } catch (err) {
      setError('Failed to add company document');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Knowledge Base Management
        </Typography>
        
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange}>
            <Tab label="Historical Tickets" />
            <Tab label="Company Documentation" />
          </Tabs>
        </Box>
        
        {activeTab === 0 && (
          <Box>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h6" component="h2" gutterBottom>
                Add Historical Ticket
              </Typography>
              
              <Box component="form" onSubmit={handleAddTicket}>
                <TextField
                  fullWidth
                  label="Ticket Text"
                  name="text"
                  value={newTicket.text}
                  onChange={handleTicketChange}
                  margin="normal"
                  required
                  multiline
                  rows={2}
                />
                
                <TextField
                  fullWidth
                  label="Solution"
                  name="solution"
                  value={newTicket.solution}
                  onChange={handleTicketChange}
                  margin="normal"
                  required
                  multiline
                  rows={3}
                />
                
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                  disabled={submitting}
                >
                  {submitting ? <CircularProgress size={24} /> : 'Add Ticket'}
                </Button>
              </Box>
            </Paper>
            
            <Typography variant="h6" component="h2" gutterBottom>
              Historical Tickets
            </Typography>
            
            <Paper elevation={1}>
              <List>
                {historicalTickets.length > 0 ? (
                  historicalTickets.map((ticket, index) => (
                    <React.Fragment key={index}>
                      <ListItem alignItems="flex-start">
                        <ListItemText
                          primary={ticket.text}
                          secondary={
                            <Typography
                              variant="body2"
                              color="text.secondary"
                              component="span"
                            >
                              Solution: {ticket.solution}
                            </Typography>
                          }
                        />
                      </ListItem>
                      {index < historicalTickets.length - 1 && <Divider />}
                    </React.Fragment>
                  ))
                ) : (
                  <ListItem>
                    <ListItemText primary="No historical tickets found" />
                  </ListItem>
                )}
              </List>
            </Paper>
          </Box>
        )}
        
        {activeTab === 1 && (
          <Box>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h6" component="h2" gutterBottom>
                Add Company Document
              </Typography>
              
              <Box component="form" onSubmit={handleAddDoc}>
                <TextField
                  fullWidth
                  label="Document Title"
                  name="title"
                  value={newDoc.title}
                  onChange={handleDocChange}
                  margin="normal"
                  required
                />
                
                <TextField
                  fullWidth
                  label="Document Content"
                  name="content"
                  value={newDoc.content}
                  onChange={handleDocChange}
                  margin="normal"
                  required
                  multiline
                  rows={4}
                />
                
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                  disabled={submitting}
                >
                  {submitting ? <CircularProgress size={24} /> : 'Add Document'}
                </Button>
              </Box>
            </Paper>
            
            <Typography variant="h6" component="h2" gutterBottom>
              Company Documents
            </Typography>
            
            <Paper elevation={1}>
              <List>
                {companyDocs.length > 0 ? (
                  companyDocs.map((doc, index) => (
                    <React.Fragment key={index}>
                      <ListItem alignItems="flex-start">
                        <ListItemText
                          primary={doc.title}
                          secondary={doc.content}
                        />
                      </ListItem>
                      {index < companyDocs.length - 1 && <Divider />}
                    </React.Fragment>
                  ))
                ) : (
                  <ListItem>
                    <ListItemText primary="No company documents found" />
                  </ListItem>
                )}
              </List>
            </Paper>
          </Box>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            {error}
          </Alert>
        )}
        
        <Snackbar
          open={success}
          autoHideDuration={6000}
          onClose={() => setSuccess(false)}
        >
          <Alert severity="success" onClose={() => setSuccess(false)}>
            {successMessage}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
};

export default KnowledgeBasePage; 