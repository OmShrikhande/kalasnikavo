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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tooltip,
  Badge,
  Fab,
  AppBar,
  Toolbar,
  ListItemIcon,
  CardActions,
  Stack,
  ButtonGroup,
  Menu,
  MenuItem,
  ListItemAvatar,
  useTheme,
  alpha,
  styled,
  keyframes,
  Slide,
  Fade,
  Zoom,
  Grow,
  Tab,
  Tabs,
  Backdrop,
  Modal,
  CardMedia
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
  Info as InfoIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Notifications as NotificationsIcon,
  Face as FaceIcon,
  Fingerprint as FingerprintIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  MoreVert as MoreVertIcon,
  FilterList as FilterListIcon,
  Sort as SortIcon,
  Search as SearchIcon,
  ViewModule as ViewGridIcon,
  ViewList as ViewListIcon,
  Refresh as RefreshIcon,
  NavigateNext as NavigateNextIcon,
  Home as HomeIcon,
  AccountCircle as AccountCircleIcon,
  Build as BuildIcon,
  Speed as SpeedIcon,
  Assessment as AssessmentIcon,
  Group as GroupIcon,
  Business as BusinessIcon,
  School as SchoolIcon,
  Work as WorkIcon,
  StarRate as StarRateIcon,
  TrendingDown as TrendingDownIcon,
  Today as TodayIcon,
  Event as EventIcon,
  CalendarToday as CalendarTodayIcon,
  AccessTime as AccessTimeIcon,
  Update as UpdateIcon,
  CloudDone as CloudDoneIcon,
  CloudQueue as CloudQueueIcon,
  FlashOn as FlashOnIcon,
  Psychology as PsychologyIcon,
  Lightbulb as LightbulbIcon,
  EmojiObjects as EmojiObjectsIcon,
  Celebration as CelebrationIcon,
  Palette as PaletteIcon,
  Brush as BrushIcon,
  AutoAwesome as AutoAwesomeIcon,
  Whatshot as WhatshotIcon,
  LocalFireDepartment as LocalFireDepartmentIcon,
  Bolt as BoltIcon,
  Highlight as HighlightIcon,
  BlurOn as BlurOnIcon,
  ColorLens as ColorLensIcon
} from '@mui/icons-material';
import axios from 'axios';

// Styled components with advanced animations and gradients
const StyledDashboard = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  background: `linear-gradient(135deg, 
    ${theme.palette.primary.main}08 0%, 
    ${theme.palette.secondary.main}08 50%, 
    ${theme.palette.primary.main}08 100%)`,
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `radial-gradient(circle at 20% 20%, ${theme.palette.primary.main}10 0%, transparent 50%),
                 radial-gradient(circle at 80% 80%, ${theme.palette.secondary.main}10 0%, transparent 50%)`,
    pointerEvents: 'none',
    zIndex: 0
  }
}));

const GlowingCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  background: `linear-gradient(145deg, 
    ${theme.palette.background.paper}f0 0%, 
    ${theme.palette.background.paper}ff 100%)`,
  backdropFilter: 'blur(20px)',
  borderRadius: 20,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: `0 20px 40px ${alpha(theme.palette.primary.main, 0.15)}`,
    '&::before': {
      opacity: 1,
    }
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `linear-gradient(145deg, 
      ${alpha(theme.palette.primary.main, 0.05)} 0%, 
      ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
    borderRadius: 20,
    opacity: 0,
    transition: 'opacity 0.3s ease',
    pointerEvents: 'none'
  }
}));

const PulsatingIcon = styled(Box)(({ theme }) => ({
  animation: 'pulse 2s infinite',
  '@keyframes pulse': {
    '0%': {
      transform: 'scale(1)',
      opacity: 1,
    },
    '50%': {
      transform: 'scale(1.05)',
      opacity: 0.8,
    },
    '100%': {
      transform: 'scale(1)',
      opacity: 1,
    }
  }
}));

const GradientText = styled(Typography)(({ theme }) => ({
  background: `linear-gradient(45deg, 
    ${theme.palette.primary.main}, 
    ${theme.palette.secondary.main})`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
  fontWeight: 'bold',
}));

const AnimatedButton = styled(Button)(({ theme }) => ({
  position: 'relative',
  overflow: 'hidden',
  borderRadius: 25,
  transition: 'all 0.3s ease',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: `linear-gradient(90deg, 
      transparent, 
      ${alpha(theme.palette.common.white, 0.3)}, 
      transparent)`,
    transition: 'left 0.5s ease',
  },
  '&:hover::before': {
    left: '100%',
  },
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: `0 10px 20px ${alpha(theme.palette.primary.main, 0.3)}`,
  }
}));

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  background: `linear-gradient(135deg, 
    ${alpha(theme.palette.primary.main, 0.9)} 0%, 
    ${alpha(theme.palette.secondary.main, 0.9)} 100%)`,
  backdropFilter: 'blur(20px)',
  borderRadius: '0 0 25px 25px',
  boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.3)}`,
}));

const DocumentCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  background: `linear-gradient(145deg, 
    ${theme.palette.background.paper}f8 0%, 
    ${theme.palette.background.paper}ff 100%)`,
  borderRadius: 16,
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  overflow: 'hidden',
  '&:hover': {
    transform: 'translateY(-4px) scale(1.02)',
    boxShadow: `0 12px 24px ${alpha(theme.palette.primary.main, 0.12)}`,
    '& .doc-actions': {
      opacity: 1,
      transform: 'translateY(0)',
    }
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 4,
    background: `linear-gradient(90deg, 
      ${theme.palette.primary.main}, 
      ${theme.palette.secondary.main})`,
  }
}));

const StatsCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  background: `linear-gradient(135deg, 
    ${theme.palette.background.paper}f0 0%, 
    ${theme.palette.background.paper}ff 100%)`,
  borderRadius: 20,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  overflow: 'hidden',
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-6px)',
    boxShadow: `0 16px 32px ${alpha(theme.palette.primary.main, 0.15)}`,
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `linear-gradient(135deg, 
      ${alpha(theme.palette.primary.main, 0.03)} 0%, 
      ${alpha(theme.palette.secondary.main, 0.03)} 100%)`,
    pointerEvents: 'none'
  }
}));

const FloatingActionButton = styled(Fab)(({ theme }) => ({
  position: 'fixed',
  bottom: 24,
  right: 24,
  background: `linear-gradient(135deg, 
    ${theme.palette.primary.main} 0%, 
    ${theme.palette.secondary.main} 100%)`,
  color: theme.palette.common.white,
  boxShadow: `0 8px 24px ${alpha(theme.palette.primary.main, 0.4)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'scale(1.1) rotate(5deg)',
    boxShadow: `0 12px 28px ${alpha(theme.palette.primary.main, 0.5)}`,
  }
}));

// Animation keyframes
const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const slideInRight = keyframes`
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

export default function Dashboard({ username, onLogout }) {
  const [documents, setDocuments] = useState([]);
  const [docUploadLoading, setDocUploadLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('grid');
  const [profileMenuAnchor, setProfileMenuAnchor] = useState(null);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [documentDetailsOpen, setDocumentDetailsOpen] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const theme = useTheme();

  const fetchDocuments = useCallback(async () => {
    setRefreshing(true);
    try {
      const res = await axios.get(`/api/user/docs?username=${encodeURIComponent(username)}`);
      setDocuments(res.data.docs || []);
    } catch {
      setDocuments([]);
    } finally {
      setRefreshing(false);
    }
  }, [username]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const getFileHash = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await window.crypto.subtle.digest('SHA-256', arrayBuffer);
    return Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  };

  const handleDocUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setDocUploadLoading(true);
    try {
      const hash = await getFileHash(file);
      const form = new FormData();
      form.append('username', username);
      form.append('doc', file);
      form.append('hash', hash);
      
      await axios.post('/api/user/docs', form);
      setSnackbar({ 
        open: true, 
        message: `${file.name} uploaded successfully!`, 
        severity: 'success' 
      });
      await fetchDocuments();
    } catch (error) {
      setSnackbar({ 
        open: true, 
        message: 'Upload failed. Please try again.', 
        severity: 'error' 
      });
    } finally {
      setDocUploadLoading(false);
    }
  };

  const handleDocDelete = async (docName) => {
    try {
      await axios.delete(`/api/user/docs?username=${encodeURIComponent(username)}&doc=${encodeURIComponent(docName)}`);
      setSnackbar({ 
        open: true, 
        message: `${docName} deleted successfully!`, 
        severity: 'success' 
      });
      await fetchDocuments();
    } catch (error) {
      setSnackbar({ 
        open: true, 
        message: 'Delete failed. Please try again.', 
        severity: 'error' 
      });
    }
  };

  const getFileIcon = (filename) => {
    const extension = filename.split('.').pop().toLowerCase();
    switch (extension) {
      case 'pdf': return <PdfIcon color="error" />;
      case 'doc': case 'docx': return <DocIcon color="primary" />;
      case 'jpg': case 'jpeg': case 'png': case 'gif': return <ImageIcon color="success" />;
      case 'mp4': case 'avi': case 'mov': return <VideoIcon color="secondary" />;
      case 'mp3': case 'wav': case 'aac': return <AudioIcon color="warning" />;
      case 'zip': case 'rar': case '7z': return <ArchiveIcon color="info" />;
      default: return <FileIcon color="disabled" />;
    }
  };

  const getFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const filteredDocuments = documents.filter(doc =>
    doc.filename?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.original_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const stats = {
    totalDocuments: documents.length,
    totalSize: documents.reduce((sum, doc) => sum + (doc.file_size || 0), 0),
    recentUploads: documents.filter(doc => {
      const uploadDate = new Date(doc.created_at);
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      return uploadDate > weekAgo;
    }).length,
    documentTypes: [...new Set(documents.map(doc => 
      doc.original_name?.split('.').pop().toLowerCase()
    ))].length
  };

  const handleViewDocument = (doc) => {
    setSelectedDocument(doc);
    setDocumentDetailsOpen(true);
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDocuments();
    setSnackbar({ 
      open: true, 
      message: 'Documents refreshed!', 
      severity: 'info' 
    });
  };

  return (
    <StyledDashboard>
      {/* Modern App Bar */}
      <StyledAppBar position="fixed" elevation={0}>
        <Toolbar>
          <PulsatingIcon sx={{ mr: 2 }}>
            <SecurityIcon sx={{ fontSize: 32 }} />
          </PulsatingIcon>
          
          <GradientText variant="h6" sx={{ flexGrow: 1 }}>
            Biometric Dashboard
          </GradientText>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Badge badgeContent={documents.length} color="secondary">
              <NotificationsIcon />
            </Badge>
            
            <Avatar
              onClick={(e) => setProfileMenuAnchor(e.currentTarget)}
              sx={{ 
                cursor: 'pointer',
                background: `linear-gradient(135deg, 
                  ${theme.palette.primary.main}, 
                  ${theme.palette.secondary.main})`,
                '&:hover': {
                  transform: 'scale(1.1)',
                }
              }}
            >
              {username.charAt(0).toUpperCase()}
            </Avatar>
          </Box>
        </Toolbar>
      </StyledAppBar>

      {/* Profile Menu */}
      <Menu
        anchorEl={profileMenuAnchor}
        open={Boolean(profileMenuAnchor)}
        onClose={() => setProfileMenuAnchor(null)}
        PaperProps={{
          sx: {
            background: `linear-gradient(135deg, 
              ${theme.palette.background.paper}f0 0%, 
              ${theme.palette.background.paper}ff 100%)`,
            backdropFilter: 'blur(20px)',
            borderRadius: 2,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
          }
        }}
      >
        <MenuItem onClick={() => setProfileMenuAnchor(null)}>
          <ListItemIcon><AccountCircleIcon /></ListItemIcon>
          Profile
        </MenuItem>
        <MenuItem onClick={() => setProfileMenuAnchor(null)}>
          <ListItemIcon><SettingsIcon /></ListItemIcon>
          Settings
        </MenuItem>
        <Divider />
        <MenuItem onClick={onLogout}>
          <ListItemIcon><LogoutIcon color="error" /></ListItemIcon>
          Logout
        </MenuItem>
      </Menu>

      {/* Main Content */}
      <Box sx={{ mt: 10, p: 3 }}>
        <Container maxWidth="xl">
          {/* Welcome Section */}
          <Fade in timeout={1000}>
            <Box sx={{ mb: 4 }}>
              <Grid container alignItems="center" spacing={3}>
                <Grid item xs={12} md={8}>
                  <Box sx={{ animation: `${fadeInUp} 1s ease-out` }}>
                    <Typography variant="h3" sx={{ mb: 1, fontWeight: 'bold' }}>
                      Welcome back, {' '}
                      <GradientText variant="h3" component="span">
                        {username}
                      </GradientText>
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                      Your secure document management center
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'flex-end',
                    animation: `${slideInRight} 1s ease-out`
                  }}>
                    <PulsatingIcon>
                      <Avatar
                        sx={{ 
                          width: 80, 
                          height: 80,
                          background: `linear-gradient(135deg, 
                            ${theme.palette.primary.main}, 
                            ${theme.palette.secondary.main})`,
                          fontSize: 32,
                          fontWeight: 'bold'
                        }}
                      >
                        {username.charAt(0).toUpperCase()}
                      </Avatar>
                    </PulsatingIcon>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          </Fade>

          {/* Statistics Cards */}
          <Grow in timeout={1200}>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={6} md={3}>
                <StatsCard>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ 
                        bgcolor: alpha(theme.palette.primary.main, 0.1),
                        color: theme.palette.primary.main,
                        mr: 2
                      }}>
                        <StorageIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                          {stats.totalDocuments}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Total Documents
                        </Typography>
                      </Box>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(stats.totalDocuments * 10, 100)} 
                      sx={{ borderRadius: 2 }}
                    />
                  </CardContent>
                </StatsCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatsCard>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ 
                        bgcolor: alpha(theme.palette.success.main, 0.1),
                        color: theme.palette.success.main,
                        mr: 2
                      }}>
                        <CloudDoneIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                          {getFileSize(stats.totalSize)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Total Size
                        </Typography>
                      </Box>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(stats.totalSize / 1024 / 1024 * 2, 100)} 
                      color="success"
                      sx={{ borderRadius: 2 }}
                    />
                  </CardContent>
                </StatsCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatsCard>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ 
                        bgcolor: alpha(theme.palette.warning.main, 0.1),
                        color: theme.palette.warning.main,
                        mr: 2
                      }}>
                        <TrendingUpIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                          {stats.recentUploads}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Recent Uploads
                        </Typography>
                      </Box>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(stats.recentUploads * 20, 100)} 
                      color="warning"
                      sx={{ borderRadius: 2 }}
                    />
                  </CardContent>
                </StatsCard>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <StatsCard>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ 
                        bgcolor: alpha(theme.palette.info.main, 0.1),
                        color: theme.palette.info.main,
                        mr: 2
                      }}>
                        <AssessmentIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                          {stats.documentTypes}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          File Types
                        </Typography>
                      </Box>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(stats.documentTypes * 25, 100)} 
                      color="info"
                      sx={{ borderRadius: 2 }}
                    />
                  </CardContent>
                </StatsCard>
              </Grid>
            </Grid>
          </Grow>

          {/* Document Management Section */}
          <Slide in direction="up" timeout={1500}>
            <GlowingCard>
              <CardContent>
                {/* Header with Actions */}
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  mb: 3
                }}>
                  <Box>
                    <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 1 }}>
                      Document Management
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Upload, organize, and manage your secure documents
                    </Typography>
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="Refresh">
                      <IconButton onClick={handleRefresh} disabled={refreshing}>
                        <RefreshIcon sx={{ 
                          animation: refreshing ? 'spin 1s linear infinite' : 'none',
                          '@keyframes spin': {
                            '0%': { transform: 'rotate(0deg)' },
                            '100%': { transform: 'rotate(360deg)' }
                          }
                        }} />
                      </IconButton>
                    </Tooltip>
                    
                    <Tooltip title="Grid View">
                      <IconButton 
                        onClick={() => setViewMode('grid')}
                        color={viewMode === 'grid' ? 'primary' : 'default'}
                      >
                        <ViewGridIcon />
                      </IconButton>
                    </Tooltip>
                    
                    <Tooltip title="List View">
                      <IconButton 
                        onClick={() => setViewMode('list')}
                        color={viewMode === 'list' ? 'primary' : 'default'}
                      >
                        <ViewListIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </Box>

                {/* Upload Section */}
                <Card sx={{ 
                  mb: 3, 
                  background: `linear-gradient(135deg, 
                    ${alpha(theme.palette.primary.main, 0.05)} 0%, 
                    ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
                  border: `2px dashed ${alpha(theme.palette.primary.main, 0.2)}`,
                  borderRadius: 3
                }}>
                  <CardContent sx={{ textAlign: 'center', py: 4 }}>
                    <PulsatingIcon sx={{ mb: 2 }}>
                      <CloudUploadIcon sx={{ fontSize: 48, color: theme.palette.primary.main }} />
                    </PulsatingIcon>
                    
                    <Typography variant="h6" sx={{ mb: 1 }}>
                      Upload Documents
                    </Typography>
                    
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                      Drag and drop files here or click to browse
                    </Typography>
                    
                    <AnimatedButton
                      variant="contained"
                      component="label"
                      startIcon={<UploadFileIcon />}
                      disabled={docUploadLoading}
                      size="large"
                      sx={{ borderRadius: 3, px: 4 }}
                    >
                      {docUploadLoading ? 'Uploading...' : 'Choose Files'}
                      <input 
                        type="file" 
                        hidden 
                        onChange={handleDocUpload}
                        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.gif,.mp4,.avi,.mov,.mp3,.wav,.zip,.rar"
                      />
                    </AnimatedButton>
                    
                    {docUploadLoading && (
                      <Box sx={{ mt: 2 }}>
                        <CircularProgress size={24} />
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          Processing your file...
                        </Typography>
                      </Box>
                    )}
                  </CardContent>
                </Card>

                {/* Search and Filter */}
                <Box sx={{ mb: 3 }}>
                  <TextField
                    fullWidth
                    placeholder="Search documents..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    InputProps={{
                      startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                      sx: { 
                        borderRadius: 3,
                        background: alpha(theme.palette.background.paper, 0.8),
                        backdropFilter: 'blur(10px)'
                      }
                    }}
                  />
                </Box>

                {/* Documents Display */}
                {filteredDocuments.length === 0 ? (
                  <Box sx={{ textAlign: 'center', py: 8 }}>
                    <PulsatingIcon sx={{ mb: 2 }}>
                      <FolderIcon sx={{ fontSize: 64, color: 'text.secondary' }} />
                    </PulsatingIcon>
                    <Typography variant="h6" color="text.secondary">
                      {searchTerm ? 'No documents found' : 'No documents uploaded yet'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {searchTerm ? 'Try adjusting your search terms' : 'Upload your first document to get started'}
                    </Typography>
                  </Box>
                ) : (
                  <Grid container spacing={3}>
                    {filteredDocuments.map((doc, index) => (
                      <Grid item xs={12} sm={6} md={4} key={doc.filename || index}>
                        <Grow in timeout={500 + index * 100}>
                          <DocumentCard>
                            <CardContent>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                <Avatar sx={{ 
                                  mr: 2,
                                  bgcolor: alpha(theme.palette.primary.main, 0.1)
                                }}>
                                  {getFileIcon(doc.original_name || doc.filename)}
                                </Avatar>
                                <Box sx={{ flex: 1, minWidth: 0 }}>
                                  <Typography variant="subtitle1" sx={{ 
                                    fontWeight: 'bold',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    whiteSpace: 'nowrap'
                                  }}>
                                    {doc.original_name || doc.filename}
                                  </Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    {getFileSize(doc.file_size || 0)}
                                  </Typography>
                                </Box>
                              </Box>
                              
                              <Box sx={{ mb: 2 }}>
                                <Typography variant="caption" color="text.secondary">
                                  Uploaded: {new Date(doc.created_at).toLocaleDateString()}
                                </Typography>
                              </Box>
                              
                              <Box sx={{ mb: 2 }}>
                                <Chip 
                                  label={doc.mime_type || 'Unknown type'}
                                  size="small"
                                  color="primary"
                                  variant="outlined"
                                />
                              </Box>
                            </CardContent>
                            
                            <CardActions 
                              className="doc-actions"
                              sx={{ 
                                opacity: 0,
                                transform: 'translateY(10px)',
                                transition: 'all 0.3s ease',
                                justifyContent: 'space-between'
                              }}
                            >
                              <ButtonGroup variant="outlined" size="small">
                                <Button
                                  startIcon={<VisibilityIcon />}
                                  onClick={() => handleViewDocument(doc)}
                                >
                                  View
                                </Button>
                                <Button
                                  startIcon={<DownloadIcon />}
                                  href={`/uploads/${doc.filename}`}
                                  target="_blank"
                                  rel="noopener"
                                >
                                  Download
                                </Button>
                              </ButtonGroup>
                              
                              <IconButton
                                color="error"
                                onClick={() => handleDocDelete(doc.filename)}
                                size="small"
                              >
                                <DeleteIcon />
                              </IconButton>
                            </CardActions>
                          </DocumentCard>
                        </Grow>
                      </Grid>
                    ))}
                  </Grid>
                )}
              </CardContent>
            </GlowingCard>
          </Slide>
        </Container>
      </Box>

      {/* Document Details Modal */}
      <Modal
        open={documentDetailsOpen}
        onClose={() => setDocumentDetailsOpen(false)}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
          sx: { backdropFilter: 'blur(10px)' }
        }}
      >
        <Fade in={documentDetailsOpen}>
          <Box sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: { xs: '90%', sm: 500 },
            bgcolor: 'background.paper',
            borderRadius: 3,
            boxShadow: 24,
            p: 4,
            maxHeight: '80vh',
            overflow: 'auto'
          }}>
            {selectedDocument && (
              <>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                  Document Details
                </Typography>
                
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>Name:</strong> {selectedDocument.original_name || selectedDocument.filename}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>Size:</strong> {getFileSize(selectedDocument.file_size || 0)}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>Uploaded:</strong> {new Date(selectedDocument.created_at).toLocaleString()}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <strong>Type:</strong> {selectedDocument.mime_type || 'Unknown'}
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => setDocumentDetailsOpen(false)}
                  >
                    Close
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<DownloadIcon />}
                    href={`/uploads/${selectedDocument.filename}`}
                    target="_blank"
                    rel="noopener"
                  >
                    Download
                  </Button>
                </Box>
              </>
            )}
          </Box>
        </Fade>
      </Modal>

      {/* Floating Action Button */}
      <FloatingActionButton
        onClick={() => document.querySelector('input[type="file"]').click()}
        disabled={docUploadLoading}
      >
        <AddIcon />
      </FloatingActionButton>

      {/* Snackbar */}
      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={6000} 
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert 
          severity={snackbar.severity} 
          sx={{ 
            width: '100%',
            borderRadius: 2,
            backdropFilter: 'blur(10px)'
          }}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </StyledDashboard>
  );
}