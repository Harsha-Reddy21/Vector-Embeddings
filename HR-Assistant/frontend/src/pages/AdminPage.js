import React, { useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Alert,
  CircularProgress,
  Snackbar,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadDocuments } from '../services/api';

const AdminPage = () => {
  const [files, setFiles] = useState([]);
  const [category, setCategory] = useState('');
  const [newCategory, setNewCategory] = useState('');
  const [documentType, setDocumentType] = useState('policy');
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info',
  });

  const documentTypes = [
    { value: 'policy', label: 'Policy Document' },
    { value: 'handbook', label: 'Employee Handbook' },
    { value: 'benefits', label: 'Benefits Information' },
    { value: 'procedure', label: 'Procedure Document' },
    { value: 'form', label: 'Form' },
  ];

  const predefinedCategories = [
    'Benefits',
    'Leave Policy',
    'Compensation',
    'Remote Work',
    'Code of Conduct',
    'Onboarding',
    'Offboarding',
    'Other',
  ];

  const onDrop = useCallback((acceptedFiles) => {
    // Filter out any non-document files
    const validFiles = acceptedFiles.filter(
      (file) =>
        file.type === 'application/pdf' ||
        file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
        file.type === 'text/plain'
    );

    if (validFiles.length !== acceptedFiles.length) {
      setSnackbar({
        open: true,
        message: 'Some files were rejected. Only PDF, DOCX, and TXT files are supported.',
        severity: 'warning',
      });
    }

    setFiles(validFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    multiple: true,
  });

  const handleUpload = async () => {
    if (files.length === 0) {
      setSnackbar({
        open: true,
        message: 'Please select at least one file to upload',
        severity: 'error',
      });
      return;
    }

    if (!category && !newCategory) {
      setSnackbar({
        open: true,
        message: 'Please select or create a category',
        severity: 'error',
      });
      return;
    }

    const selectedCategory = newCategory || category;

    try {
      setLoading(true);
      await uploadDocuments(files, documentType, selectedCategory);
      
      setSnackbar({
        open: true,
        message: 'Documents uploaded successfully',
        severity: 'success',
      });
      
      // Reset form
      setFiles([]);
      setCategory('');
      setNewCategory('');
      
    } catch (error) {
      console.error('Error uploading documents:', error);
      setSnackbar({
        open: true,
        message: 'Failed to upload documents. Please try again.',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Admin Panel
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload and manage HR documents for the knowledge assistant.
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Upload Documents
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed #cccccc',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? 'rgba(25, 118, 210, 0.04)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(25, 118, 210, 0.04)',
                },
              }}
            >
              <input {...getInputProps()} />
              <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
              {isDragActive ? (
                <Typography>Drop the files here...</Typography>
              ) : (
                <Typography>
                  Drag and drop files here, or click to select files
                </Typography>
              )}
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Supported formats: PDF, DOCX, TXT
              </Typography>
            </Box>
          </Grid>

          {files.length > 0 && (
            <Grid item xs={12}>
              <Alert severity="info">
                {files.length} file{files.length > 1 ? 's' : ''} selected:
                <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px' }}>
                  {files.map((file, index) => (
                    <li key={index}>{file.name}</li>
                  ))}
                </ul>
              </Alert>
            </Grid>
          )}

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel id="document-type-label">Document Type</InputLabel>
              <Select
                labelId="document-type-label"
                id="document-type"
                value={documentType}
                label="Document Type"
                onChange={(e) => setDocumentType(e.target.value)}
              >
                {documentTypes.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    {type.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel id="category-label">Category</InputLabel>
              <Select
                labelId="category-label"
                id="category"
                value={category}
                label="Category"
                onChange={(e) => setCategory(e.target.value)}
                disabled={!!newCategory}
              >
                {predefinedCategories.map((cat) => (
                  <MenuItem key={cat} value={cat}>
                    {cat}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Or create a new category:
            </Typography>
            <TextField
              fullWidth
              label="New Category"
              variant="outlined"
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              disabled={!!category}
              helperText="Leave empty to use a predefined category"
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              disabled={loading || files.length === 0}
              startIcon={loading ? <CircularProgress size={20} /> : <CloudUploadIcon />}
            >
              {loading ? 'Uploading...' : 'Upload Documents'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AdminPage; 