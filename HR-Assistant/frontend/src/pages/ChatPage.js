import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { queryAssistant, getCategories } from '../services/api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Load categories when component mounts
    const loadCategories = async () => {
      try {
        const categoriesData = await getCategories();
        setCategories(categoriesData || []);
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    };

    loadCategories();
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages change
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      text: input,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await queryAssistant(
        input,
        selectedCategories.length > 0 ? selectedCategories : null
      );

      const assistantMessage = {
        text: response.answer,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        sources: response.sources,
        category: response.category,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error querying assistant:', error);
      
      const errorMessage = {
        text: 'Sorry, I encountered an error while processing your request. Please try again later.',
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true,
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCategoryChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedCategories(
      typeof value === 'string' ? value.split(',') : value
    );
  };

  return (
    <Box sx={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ mb: 2 }}>
        <Typography variant="h5" gutterBottom>
          HR Knowledge Assistant
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Ask me anything about company policies, benefits, or HR procedures.
        </Typography>
        
        <FormControl sx={{ width: '100%', mb: 2 }}>
          <InputLabel id="category-select-label">Filter by Category</InputLabel>
          <Select
            labelId="category-select-label"
            id="category-select"
            multiple
            value={selectedCategories}
            onChange={handleCategoryChange}
            input={<OutlinedInput label="Filter by Category" />}
            renderValue={(selected) => (
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {selected.map((value) => (
                  <Chip key={value} label={value} />
                ))}
              </Box>
            )}
          >
            {categories.map((category) => (
              <MenuItem key={category} value={category}>
                {category}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Paper
        ref={chatContainerRef}
        elevation={3}
        className="chat-container"
        sx={{ 
          flexGrow: 1, 
          mb: 2, 
          p: 2, 
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {messages.length === 0 ? (
          <Box 
            sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              justifyContent: 'center',
              height: '100%',
              color: 'text.secondary'
            }}
          >
            <Typography variant="h6">
              Welcome to HR Knowledge Assistant
            </Typography>
            <Typography variant="body1">
              How can I help you today?
            </Typography>
          </Box>
        ) : (
          messages.map((message, index) => (
            <Box
              key={index}
              className={`message ${message.sender === 'user' ? 'user-message' : 'assistant-message'}`}
              sx={{
                alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: message.sender === 'user' ? 'primary.light' : 'grey.100',
                borderRadius: 2,
                p: 2,
                mb: 2,
                maxWidth: '80%',
              }}
            >
              <Typography variant="body1">{message.text}</Typography>
              {message.sources && (
                <Box className="source-citation" sx={{ mt: 1, fontSize: '0.8rem', color: 'text.secondary' }}>
                  <Typography variant="caption">Sources:</Typography>
                  <ul style={{ margin: '4px 0', paddingLeft: '20px' }}>
                    {message.sources.map((source, idx) => (
                      <li key={idx}>
                        <Typography variant="caption">{source}</Typography>
                      </li>
                    ))}
                  </ul>
                </Box>
              )}
              {message.category && (
                <Chip 
                  label={`Category: ${message.category}`} 
                  size="small" 
                  sx={{ mt: 1 }} 
                />
              )}
            </Box>
          ))
        )}
      </Paper>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask a question about HR policies..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
          multiline
          maxRows={3}
        />
        <Button
          variant="contained"
          color="primary"
          endIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
          onClick={handleSend}
          disabled={loading || !input.trim()}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatPage; 