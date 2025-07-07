import React, { useState } from 'react';
import { Container, Box, Typography, Button, TextField, Paper, Stepper, Step, StepLabel, Snackbar, Alert } from '@mui/material';
import axios from 'axios';

const steps = ['Face Recognition', 'Fingerprint Recognition'];

export default function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [username, setUsername] = useState('');
  const [faceFile, setFaceFile] = useState(null);
  const [fpFile, setFpFile] = useState(null);
  const [registerMode, setRegisterMode] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });

  const handleRegister = async () => {
    if (!username || !faceFile || !fpFile) {
      setSnackbar({ open: true, message: 'All fields required', severity: 'error' });
      return;
    }
    const form = new FormData();
    form.append('username', username);
    form.append('face', faceFile);
    form.append('fingerprint', fpFile);
    try {
      await axios.post('/api/register', form);
      setSnackbar({ open: true, message: 'Registration successful!', severity: 'success' });
      setRegisterMode(false);
    } catch (e) {
      setSnackbar({ open: true, message: e.response?.data?.error || 'Registration failed', severity: 'error' });
    }
  };

  const handleFaceAuth = async () => {
    if (!username || !faceFile) {
      setSnackbar({ open: true, message: 'Username and face image required', severity: 'error' });
      return;
    }
    const form = new FormData();
    form.append('username', username);
    form.append('face', faceFile);
    try {
      await axios.post('/api/auth/face', form);
      setActiveStep(1);
      setSnackbar({ open: true, message: 'Face recognized! Please provide fingerprint.', severity: 'success' });
    } catch (e) {
      setSnackbar({ open: true, message: e.response?.data?.error || 'Face not recognized', severity: 'error' });
    }
  };

  const handleFpAuth = async () => {
    if (!username || !fpFile) {
      setSnackbar({ open: true, message: 'Username and fingerprint required', severity: 'error' });
      return;
    }
    const form = new FormData();
    form.append('username', username);
    form.append('fingerprint', fpFile);
    try {
      await axios.post('/api/auth/fingerprint', form);
      setSnackbar({ open: true, message: 'Access granted!', severity: 'success' });
      setActiveStep(0);
    } catch (e) {
      setSnackbar({ open: true, message: e.response?.data?.error || 'Fingerprint not recognized', severity: 'error' });
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Dual Biometric Authentication
        </Typography>
        <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
          {steps.map(label => (
            <Step key={label}><StepLabel>{label}</StepLabel></Step>
          ))}
        </Stepper>
        <Box sx={{ mb: 2 }}>
          <TextField
            label="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            fullWidth
            sx={{ mb: 2 }}
          />
          <Button onClick={() => setRegisterMode(!registerMode)} sx={{ mb: 2 }}>
            {registerMode ? 'Back to Login' : 'Register New User'}
          </Button>
        </Box>
        {registerMode ? (
          <Box>
            <Button variant="contained" component="label" fullWidth sx={{ mb: 2 }}>
              Upload Face Image
              <input type="file" hidden accept="image/*" onChange={e => setFaceFile(e.target.files[0])} />
            </Button>
            <Button variant="contained" component="label" fullWidth sx={{ mb: 2 }}>
              Upload Fingerprint
              <input type="file" hidden accept=".bmp" onChange={e => setFpFile(e.target.files[0])} />
            </Button>
            <Button variant="contained" color="primary" fullWidth onClick={handleRegister}>
              Register
            </Button>
          </Box>
        ) : (
          <Box>
            {activeStep === 0 && (
              <>
                <Button variant="contained" component="label" fullWidth sx={{ mb: 2 }}>
                  Upload Face Image
                  <input type="file" hidden accept="image/*" onChange={e => setFaceFile(e.target.files[0])} />
                </Button>
                <Button variant="contained" color="primary" fullWidth onClick={handleFaceAuth}>
                  Authenticate Face
                </Button>
              </>
            )}
            {activeStep === 1 && (
              <>
                <Button variant="contained" component="label" fullWidth sx={{ mb: 2 }}>
                  Upload Fingerprint
                  <input type="file" hidden accept=".bmp" onChange={e => setFpFile(e.target.files[0])} />
                </Button>
                <Button variant="contained" color="primary" fullWidth onClick={handleFpAuth}>
                  Authenticate Fingerprint
                </Button>
              </>
            )}
          </Box>
        )}
      </Paper>
      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>{snackbar.message}</Alert>
      </Snackbar>
    </Container>
  );
}
