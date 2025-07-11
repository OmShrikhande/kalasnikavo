import React, { useEffect, useState, useCallback } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Snackbar,
  Alert,
  CircularProgress,
  Grid,
  Box,
  Avatar,
  Chip,
  LinearProgress,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tooltip,
  Badge,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Fab
} from '@mui/material';
import {
  UploadFile as UploadFileIcon,
  Delete as DeleteIcon,
  Logout as LogoutIcon,
  Security as SecurityIcon,
  Analytics as AnalyticsIcon,
  History as HistoryIcon,
  CloudUpload as CloudUploadIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Add as AddIcon,
  Folder as FolderIcon,
  InsertDriveFile as FileIcon,
  Image as ImageIcon,
  PictureAsPdf as PdfIcon,
  Description as DocIcon,
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  Archive as ArchiveIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
  Schedule as ScheduleIcon,
  Storage as StorageIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

export default function Dashboard({ username, onLogout }) {
  const [documents, setDocuments] = useState([]);
  const [docUploadLoading, setDocUploadLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });

  const fetchDocuments = async () => {
    try {
      const res = await axios.get(`/api/user/docs?username=${encodeURIComponent(username)}`);
      setDocuments(res.data.docs || []);
    } catch {
      setDocuments([]);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [username]);

  // Calculate SHA256 hash of file (browser)
  const getFileHash = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await window.crypto.subtle.digest('SHA-256', arrayBuffer);
    return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
  };

  const handleDocUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setDocUploadLoading(true);
    const hash = await getFileHash(file);
    const form = new FormData();
    form.append('username', username);
    form.append('doc', file);
    form.append('hash', hash);
    try {
      await axios.post('/api/user/docs', form);
      setSnackbar({ open: true, message: 'Document uploaded!', severity: 'success' });
      fetchDocuments();
    } catch {
      setSnackbar({ open: true, message: 'Upload failed', severity: 'error' });
    }
    setDocUploadLoading(false);
  };

  const handleDocDelete = async (docName) => {
    try {
      await axios.delete(`/api/user/docs?username=${encodeURIComponent(username)}&doc=${encodeURIComponent(docName)}`);
      setSnackbar({ open: true, message: 'Document deleted!', severity: 'success' });
      fetchDocuments();
    } catch {
      setSnackbar({ open: true, message: 'Delete failed', severity: 'error' });
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Paper elevation={4} sx={{ p: 4, borderRadius: 4 }}>
        <Typography variant="h4" sx={{ mb: 2 }}>Welcome, {username}</Typography>
        <IconButton color="error" onClick={onLogout} sx={{ float: 'right' }}><LogoutIcon /></IconButton>
        <Typography variant="h6" sx={{ mb: 2 }}>Your Documents</Typography>
        <Card sx={{ mb: 2, p: 2, bgcolor: "#f9f9f9" }}>
          <CardContent>
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadFileIcon />}
              disabled={docUploadLoading}
            >
              Upload Document
              <input type="file" hidden onChange={handleDocUpload} />
            </Button>
            {docUploadLoading && <CircularProgress size={24} sx={{ ml: 2 }} />}
          </CardContent>
        </Card>
        <List>
          {documents.length === 0 && <Typography>No documents uploaded yet.</Typography>}
          {documents.map(doc => (
            <ListItem key={doc.name}>
              <ListItemText
                primary={doc.name}
                secondary={`SHA256: ${doc.hash}`}
              />
              <ListItemSecondaryAction>
                <Button
                  href={`/uploads/${doc.name}`}
                  target="_blank"
                  rel="noopener"
                  size="small"
                  sx={{ mr: 1 }}
                >View</Button>
                <IconButton edge="end" color="error" onClick={() => handleDocDelete(doc.name)}>
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Paper>
      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>{snackbar.message}</Alert>
      </Snackbar>
    </Container>
  );
}
