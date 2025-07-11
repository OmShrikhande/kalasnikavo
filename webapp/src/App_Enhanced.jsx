import React, { useState, useRef, useEffect, useCallback } from "react";
import {
  Container,
  Box,
  Typography,
  Button,
  TextField,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Snackbar,
  Alert,
  CircularProgress,
  LinearProgress,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Switch,
  FormControlLabel,
  Slider,
  Badge,
  Tooltip,
  AppBar,
  Toolbar,
  ThemeProvider,
  CssBaseline,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Tabs,
  Tab,
  TabPanel,
  styled,
  alpha,
  keyframes,
  Fade,
  Slide,
  Grow,
  Zoom
} from "@mui/material";
import {
  UploadFile as UploadFileIcon,
  Delete as DeleteIcon,
  Logout as LogoutIcon,
  Security as SecurityIcon,
  Face as FaceIcon,
  Fingerprint as FingerprintIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Analytics as AnalyticsIcon,
  History as HistoryIcon,
  Notifications as NotificationsIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Camera as CameraIcon,
  Refresh as RefreshIcon,
  Save as SaveIcon,
  Shield as ShieldIcon,
  Speed as SpeedIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Memory as MemoryIcon,
  Psychology as PsychologyIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  PersonAdd as PersonAddIcon,
  Login as LoginIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
  Timeline as TimelineIcon,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
  ShowChart as ShowChartIcon,
  AutoAwesome as AutoAwesomeIcon,
  Layers as LayersIcon,
  FilterAlt as FilterAltIcon,
  Tune as TuneIcon,
  Computer as ComputerIcon,
  CloudDone as CloudDoneIcon,
  Verified as VerifiedIcon,
  LocalPolice as LocalPoliceIcon,
  LockPerson as LockPersonIcon,
  AdminPanelSettings as AdminPanelSettingsIcon
} from "@mui/icons-material";
import axios from "axios";
import Dashboard from "./Dashboard";
import theme from "./theme";

// Set axios base URL
axios.defaults.baseURL = 'http://localhost:5000';

const steps = ["Advanced Face Recognition", "Multi-Algorithm Fingerprint", "Dual Biometric Fusion"];
const MAX_FACE_IMAGES = 5;

const securityLevels = {
  'LOW': {
    label: 'Low Security',
    color: 'info',
    description: 'Basic authentication with standard algorithms',
    threshold: '70%',
    algorithms: ['deepface', 'resnet']
  },
  'MEDIUM': {
    label: 'Medium Security',
    color: 'warning',
    description: 'Enhanced authentication with multiple algorithms',
    threshold: '80%',
    algorithms: ['deepface', 'resnet', 'vgg16']
  },
  'HIGH': {
    label: 'High Security',
    color: 'error',
    description: 'Advanced authentication with fusion algorithms',
    threshold: '90%',
    algorithms: ['deepface', 'resnet', 'vgg16', 'inception']
  },
  'MAXIMUM': {
    label: 'Maximum Security',
    color: 'success',
    description: 'Military-grade authentication with all algorithms',
    threshold: '95%',
    algorithms: ['deepface', 'resnet', 'vgg16', 'inception', 'ensemble']
  }
};

// Styled components
const StyledCard = styled(Card)(({ theme, glowing }) => ({
  background: glowing ? 
    `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)` :
    theme.palette.background.paper,
  border: glowing ? `1px solid ${theme.palette.primary.main}` : 'none',
  boxShadow: glowing ? 
    `0 0 20px ${alpha(theme.palette.primary.main, 0.3)}` :
    theme.shadows[3],
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[6],
  }
}));

const AlgorithmChip = styled(Chip)(({ theme, confidence }) => ({
  margin: theme.spacing(0.5),
  backgroundColor: confidence > 90 ? 
    alpha(theme.palette.success.main, 0.2) :
    confidence > 70 ?
    alpha(theme.palette.warning.main, 0.2) :
    alpha(theme.palette.error.main, 0.2),
  color: confidence > 90 ? 
    theme.palette.success.main :
    confidence > 70 ?
    theme.palette.warning.main :
    theme.palette.error.main,
  border: `1px solid ${confidence > 90 ? 
    theme.palette.success.main :
    confidence > 70 ?
    theme.palette.warning.main :
    theme.palette.error.main}`,
  fontWeight: 'bold',
}));

const SecurityLevelChip = styled(Chip)(({ theme, level }) => ({
  backgroundColor: level === 'MAXIMUM' ? 
    alpha(theme.palette.success.main, 0.2) :
    level === 'HIGH' ?
    alpha(theme.palette.error.main, 0.2) :
    level === 'MEDIUM' ?
    alpha(theme.palette.warning.main, 0.2) :
    alpha(theme.palette.info.main, 0.2),
  color: level === 'MAXIMUM' ? 
    theme.palette.success.main :
    level === 'HIGH' ?
    theme.palette.error.main :
    level === 'MEDIUM' ?
    theme.palette.warning.main :
    theme.palette.info.main,
  fontWeight: 'bold',
  fontSize: '0.9rem',
}));

const pulseAnimation = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
`;

const PulsingProgress = styled(LinearProgress)(({ theme }) => ({
  animation: `${pulseAnimation} 2s ease-in-out infinite`,
  borderRadius: 8,
  height: 8,
}));

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export default function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [securityLevel, setSecurityLevel] = useState("MEDIUM");
  const [faceImages, setFaceImages] = useState([]);
  const [fpFile, setFpFile] = useState(null);
  const [registerMode, setRegisterMode] = useState(false);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "info",
  });
  const [loading, setLoading] = useState(false);
  const [faceAuthLoading, setFaceAuthLoading] = useState(false);
  const [fpAuthLoading, setFpAuthLoading] = useState(false);
  const [dualAuthLoading, setDualAuthLoading] = useState(false);
  const [captureStep, setCaptureStep] = useState(0);
  const [dashboard, setDashboard] = useState(false);
  const [authResults, setAuthResults] = useState(null);
  const [tabValue, setTabValue] = useState(0);
  const [systemStatus, setSystemStatus] = useState(null);
  const [showAlgorithmDetails, setShowAlgorithmDetails] = useState(false);
  const [authMode, setAuthMode] = useState('single'); // 'single' or 'dual'
  const [qualityScores, setQualityScores] = useState({});
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    fetchSystemStatus();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await axios.get('/api/system/status');
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const startCamera = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: 'user'
          } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        setSnackbar({
          open: true,
          message: "Camera access denied. Please enable camera permissions.",
          severity: "error",
        });
      }
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, 640, 480);
      canvasRef.current.toBlob(
        (blob) => {
          setFaceImages((prev) => [
            ...prev,
            new File([blob], `face_${prev.length}.jpg`, { type: "image/jpeg" }),
          ]);
          setCaptureStep((prev) => prev + 1);
        },
        "image/jpeg",
        0.95
      );
    }
  };

  const resetRegistration = () => {
    setFaceImages([]);
    setFpFile(null);
    setCaptureStep(0);
    setQualityScores({});
    stopCamera();
  };

  const handleRegister = async () => {
    if (!username || faceImages.length === 0 || !fpFile) {
      setSnackbar({
        open: true,
        message: "All fields required",
        severity: "error",
      });
      return;
    }
    
    setLoading(true);
    const form = new FormData();
    form.append("username", username);
    form.append("email", email);
    form.append("securityLevel", securityLevel);
    faceImages.forEach((img, idx) => form.append(`face_${idx}`, img));
    form.append("fingerprint", fpFile);
    
    try {
      const response = await axios.post("/api/register", form);
      setSnackbar({
        open: true,
        message: "Registration successful! You can now login.",
        severity: "success",
      });
      setRegisterMode(false);
      resetRegistration();
      setQualityScores(response.data.biometric_quality || {});
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Registration failed",
        severity: "error",
      });
    }
    setLoading(false);
  };

  const handleFaceAuth = async () => {
    if (!username || faceImages.length === 0) {
      setSnackbar({
        open: true,
        message: "Username and face image required",
        severity: "error",
      });
      return;
    }
    
    setFaceAuthLoading(true);
    const form = new FormData();
    form.append("username", username);
    form.append("face", faceImages[0]);
    
    try {
      const response = await axios.post("/api/auth/face", form);
      setAuthResults(response.data);
      setActiveStep(1);
      setSnackbar({
        open: true,
        message: `Face recognized with ${response.data.confidence.toFixed(1)}% confidence! Please provide fingerprint.`,
        severity: "success",
      });
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Face not recognized",
        severity: "error",
      });
      setAuthResults(e.response?.data || null);
    }
    setFaceAuthLoading(false);
  };

  const handleFpAuth = async () => {
    if (!username || !fpFile) {
      setSnackbar({
        open: true,
        message: "Username and fingerprint required",
        severity: "error",
      });
      return;
    }
    
    setFpAuthLoading(true);
    const form = new FormData();
    form.append("username", username);
    form.append("fingerprint", fpFile);
    
    try {
      const response = await axios.post("/api/auth/fingerprint", form);
      setAuthResults(response.data);
      setSnackbar({
        open: true,
        message: `Access granted with ${response.data.confidence.toFixed(1)}% confidence!`,
        severity: "success",
      });
      setActiveStep(0);
      setFaceImages([]);
      setFpFile(null);
      setDashboard(true);
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Fingerprint not recognized",
        severity: "error",
      });
      setAuthResults(e.response?.data || null);
    }
    setFpAuthLoading(false);
  };

  const handleDualAuth = async () => {
    if (!username || faceImages.length === 0 || !fpFile) {
      setSnackbar({
        open: true,
        message: "Username, face image, and fingerprint required",
        severity: "error",
      });
      return;
    }
    
    setDualAuthLoading(true);
    const form = new FormData();
    form.append("username", username);
    form.append("face", faceImages[0]);
    form.append("fingerprint", fpFile);
    
    try {
      const response = await axios.post("/api/auth/dual", form);
      setAuthResults(response.data);
      setSnackbar({
        open: true,
        message: `Dual authentication successful with ${response.data.fusion_score.toFixed(1)}% fusion score!`,
        severity: "success",
      });
      setActiveStep(0);
      setFaceImages([]);
      setFpFile(null);
      setDashboard(true);
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Dual authentication failed",
        severity: "error",
      });
      setAuthResults(e.response?.data || null);
    }
    setDualAuthLoading(false);
  };

  const handleLogout = () => {
    setDashboard(false);
    setUsername("");
    setEmail("");
    setActiveStep(0);
    setRegisterMode(false);
    setAuthResults(null);
  };

  const faceCaptureInstructions = [
    "Look straight at the camera with neutral expression.",
    "Turn your face slightly to the left (15-20 degrees).",
    "Turn your face slightly to the right (15-20 degrees).",
    "Look up slightly while keeping eyes on camera.",
    "Look down slightly while keeping eyes on camera.",
  ];

  const renderAlgorithmScores = (scores) => {
    if (!scores) return null;
    
    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" gutterBottom>
          Algorithm Performance:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {Object.entries(scores).map(([algorithm, score]) => (
            <AlgorithmChip
              key={algorithm}
              label={`${algorithm.toUpperCase()}: ${(score * 100).toFixed(1)}%`}
              confidence={score * 100}
              size="small"
              icon={algorithm === 'ensemble' ? <AutoAwesomeIcon /> : 
                   algorithm === 'deepface' ? <PsychologyIcon /> :
                   algorithm === 'resnet' ? <MemoryIcon /> : 
                   <ComputerIcon />}
            />
          ))}
        </Box>
      </Box>
    );
  };

  const renderQualityIndicator = (quality) => {
    const color = quality > 0.9 ? 'success' : quality > 0.7 ? 'warning' : 'error';
    return (
      <Chip
        label={`Quality: ${(quality * 100).toFixed(1)}%`}
        color={color}
        size="small"
        icon={<AssessmentIcon />}
      />
    );
  };

  if (dashboard) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Dashboard 
          username={username} 
          onLogout={handleLogout} 
          authResults={authResults}
          systemStatus={systemStatus}
        />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <StyledCard elevation={6} glowing={true}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <Avatar sx={{ bgcolor: 'primary.main', mr: 2, width: 56, height: 56 }}>
                <ShieldIcon fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h4" component="h1" gutterBottom>
                  Enhanced Biometric Authentication
                </Typography>
                <Typography variant="subtitle1" color="text.secondary">
                  Military-grade security with multi-algorithm fusion
                </Typography>
              </Box>
            </Box>

            {/* System Status */}
            {systemStatus && (
              <Accordion sx={{ mb: 3 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">
                    System Status
                    <Chip 
                      label={systemStatus.status} 
                      color="success" 
                      size="small" 
                      sx={{ ml: 2 }}
                    />
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2">
                        <strong>Active Users:</strong> {systemStatus.user_count}
                      </Typography>
                      <Typography variant="body2">
                        <strong>DeepFace Available:</strong> {systemStatus.deepface_available ? 'Yes' : 'No'}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2">
                        <strong>Face Algorithms:</strong> {systemStatus.algorithms_available?.face?.join(', ')}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Fingerprint Algorithms:</strong> {systemStatus.algorithms_available?.fingerprint?.join(', ')}
                      </Typography>
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
            )}

            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Authentication" icon={<LoginIcon />} />
              <Tab label="Registration" icon={<PersonAddIcon />} />
              <Tab label="Settings" icon={<SettingsIcon />} />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              {/* Authentication Mode Selection */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Authentication Mode
                </Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button
                    variant={authMode === 'single' ? 'contained' : 'outlined'}
                    onClick={() => setAuthMode('single')}
                    startIcon={<SecurityIcon />}
                  >
                    Single Factor
                  </Button>
                  <Button
                    variant={authMode === 'dual' ? 'contained' : 'outlined'}
                    onClick={() => setAuthMode('dual')}
                    startIcon={<LockPersonIcon />}
                  >
                    Dual Factor
                  </Button>
                </Box>
              </Box>

              {authMode === 'single' && (
                <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
                  {steps.slice(0, 2).map((label) => (
                    <Step key={label}>
                      <StepLabel>{label}</StepLabel>
                    </Step>
                  ))}
                </Stepper>
              )}

              <Box sx={{ mb: 3 }}>
                <TextField
                  label="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  fullWidth
                  sx={{ mb: 2 }}
                  InputProps={{
                    startAdornment: <PersonAddIcon sx={{ mr: 1, color: 'action.active' }} />
                  }}
                />
              </Box>

              {authMode === 'dual' ? (
                // Dual Authentication Mode
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Dual Biometric Authentication
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <StyledCard>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            <FaceIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                            Face Recognition
                          </Typography>
                          {faceImages.length === 0 ? (
                            <Box sx={{ textAlign: 'center', py: 3 }}>
                              <video
                                ref={videoRef}
                                width="320"
                                height="240"
                                autoPlay
                                style={{ borderRadius: 8, border: "1px solid #ccc" }}
                              />
                              <canvas
                                ref={canvasRef}
                                width="320"
                                height="240"
                                style={{ display: "none" }}
                              />
                              <Box sx={{ mt: 2 }}>
                                <Button
                                  variant="contained"
                                  onClick={startCamera}
                                  sx={{ mr: 1 }}
                                  startIcon={<CameraIcon />}
                                >
                                  Start Camera
                                </Button>
                                <Button
                                  variant="contained"
                                  color="secondary"
                                  onClick={captureImage}
                                  disabled={!videoRef.current?.srcObject}
                                  startIcon={<CameraIcon />}
                                >
                                  Capture
                                </Button>
                              </Box>
                            </Box>
                          ) : (
                            <Box sx={{ textAlign: 'center' }}>
                              <img
                                src={URL.createObjectURL(faceImages[0])}
                                alt="captured face"
                                style={{ width: '100%', maxWidth: 200, borderRadius: 8 }}
                              />
                              <Box sx={{ mt: 1 }}>
                                <Button
                                  variant="outlined"
                                  onClick={() => setFaceImages([])}
                                  startIcon={<DeleteIcon />}
                                >
                                  Retake
                                </Button>
                              </Box>
                            </Box>
                          )}
                        </CardContent>
                      </StyledCard>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <StyledCard>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            <FingerprintIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                            Fingerprint Recognition
                          </Typography>
                          <Button
                            variant="contained"
                            component="label"
                            fullWidth
                            sx={{ mb: 2 }}
                            startIcon={<UploadFileIcon />}
                          >
                            Upload Fingerprint
                            <input
                              type="file"
                              hidden
                              accept=".bmp,.png,.jpg,.jpeg"
                              onChange={(e) => setFpFile(e.target.files[0])}
                            />
                          </Button>
                          {fpFile && (
                            <Box sx={{ mt: 2, textAlign: 'center' }}>
                              <Typography variant="body2" gutterBottom>
                                Selected: {fpFile.name}
                              </Typography>
                              <img
                                src={URL.createObjectURL(fpFile)}
                                alt="fingerprint"
                                style={{ width: '100%', maxWidth: 200, borderRadius: 8 }}
                              />
                            </Box>
                          )}
                        </CardContent>
                      </StyledCard>
                    </Grid>
                  </Grid>
                  <Box sx={{ mt: 3, textAlign: 'center' }}>
                    <Button
                      variant="contained"
                      size="large"
                      onClick={handleDualAuth}
                      disabled={dualAuthLoading || !username || faceImages.length === 0 || !fpFile}
                      startIcon={dualAuthLoading ? <CircularProgress size={20} /> : <LocalPoliceIcon />}
                      sx={{ minWidth: 200 }}
                    >
                      {dualAuthLoading ? 'Authenticating...' : 'Dual Authentication'}
                    </Button>
                  </Box>
                </Box>
              ) : (
                // Single Authentication Mode
                <Box>
                  {activeStep === 0 && (
                    <StyledCard>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          <FaceIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                          Face Authentication
                        </Typography>
                        {faceImages.length === 0 ? (
                          <Box sx={{ textAlign: 'center', py: 3 }}>
                            <video
                              ref={videoRef}
                              width="320"
                              height="240"
                              autoPlay
                              style={{ borderRadius: 8, border: "1px solid #ccc" }}
                            />
                            <canvas
                              ref={canvasRef}
                              width="320"
                              height="240"
                              style={{ display: "none" }}
                            />
                            <Box sx={{ mt: 2 }}>
                              <Button
                                variant="contained"
                                onClick={startCamera}
                                sx={{ mr: 1 }}
                                startIcon={<CameraIcon />}
                              >
                                Start Camera
                              </Button>
                              <Button
                                variant="contained"
                                color="secondary"
                                onClick={captureImage}
                                disabled={!videoRef.current?.srcObject}
                                startIcon={<CameraIcon />}
                              >
                                Capture
                              </Button>
                            </Box>
                          </Box>
                        ) : (
                          <Box sx={{ textAlign: 'center' }}>
                            <img
                              src={URL.createObjectURL(faceImages[0])}
                              alt="captured face"
                              style={{ width: '100%', maxWidth: 200, borderRadius: 8 }}
                            />
                            <Box sx={{ mt: 2 }}>
                              <Button
                                variant="contained"
                                onClick={handleFaceAuth}
                                disabled={faceAuthLoading || !username}
                                startIcon={faceAuthLoading ? <CircularProgress size={20} /> : <FaceIcon />}
                                sx={{ mr: 1 }}
                              >
                                {faceAuthLoading ? 'Analyzing...' : 'Authenticate Face'}
                              </Button>
                              <Button
                                variant="outlined"
                                onClick={() => setFaceImages([])}
                                startIcon={<DeleteIcon />}
                              >
                                Retake
                              </Button>
                            </Box>
                          </Box>
                        )}
                      </CardContent>
                    </StyledCard>
                  )}

                  {activeStep === 1 && (
                    <StyledCard>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          <FingerprintIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                          Fingerprint Authentication
                        </Typography>
                        <Button
                          variant="contained"
                          component="label"
                          fullWidth
                          sx={{ mb: 2 }}
                          startIcon={<UploadFileIcon />}
                        >
                          Upload Fingerprint
                          <input
                            type="file"
                            hidden
                            accept=".bmp,.png,.jpg,.jpeg"
                            onChange={(e) => setFpFile(e.target.files[0])}
                          />
                        </Button>
                        {fpFile && (
                          <Box sx={{ mt: 2, textAlign: 'center' }}>
                            <Typography variant="body2" gutterBottom>
                              Selected: {fpFile.name}
                            </Typography>
                            <img
                              src={URL.createObjectURL(fpFile)}
                              alt="fingerprint"
                              style={{ width: '100%', maxWidth: 200, borderRadius: 8 }}
                            />
                            <Box sx={{ mt: 2 }}>
                              <Button
                                variant="contained"
                                onClick={handleFpAuth}
                                disabled={fpAuthLoading || !username}
                                startIcon={fpAuthLoading ? <CircularProgress size={20} /> : <FingerprintIcon />}
                              >
                                {fpAuthLoading ? 'Analyzing...' : 'Authenticate Fingerprint'}
                              </Button>
                            </Box>
                          </Box>
                        )}
                      </CardContent>
                    </StyledCard>
                  )}
                </Box>
              )}

              {/* Authentication Results */}
              {authResults && (
                <StyledCard sx={{ mt: 3 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Authentication Results
                    </Typography>
                    {authResults.success !== undefined && (
                      <Alert severity={authResults.success ? 'success' : 'error'} sx={{ mb: 2 }}>
                        {authResults.success ? 'Authentication Successful' : 'Authentication Failed'}
                      </Alert>
                    )}
                    {authResults.confidence && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          Overall Confidence: {authResults.confidence.toFixed(1)}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={authResults.confidence}
                          sx={{ mt: 1 }}
                        />
                      </Box>
                    )}
                    {authResults.fusion_score && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          Fusion Score: {authResults.fusion_score.toFixed(1)}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={authResults.fusion_score}
                          sx={{ mt: 1 }}
                        />
                      </Box>
                    )}
                    {authResults.algorithm_scores && renderAlgorithmScores(authResults.algorithm_scores)}
                    {authResults.face_result && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2">Face Recognition:</Typography>
                        {renderAlgorithmScores(authResults.face_result.algorithm_scores)}
                      </Box>
                    )}
                    {authResults.fingerprint_result && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2">Fingerprint Recognition:</Typography>
                        {renderAlgorithmScores(authResults.fingerprint_result.algorithm_scores)}
                      </Box>
                    )}
                  </CardContent>
                </StyledCard>
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              {/* Registration */}
              <Typography variant="h6" gutterBottom>
                User Registration
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <TextField
                    label="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    fullWidth
                    sx={{ mb: 2 }}
                    required
                  />
                  <TextField
                    label="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    fullWidth
                    sx={{ mb: 2 }}
                  />
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Security Level</InputLabel>
                    <Select
                      value={securityLevel}
                      onChange={(e) => setSecurityLevel(e.target.value)}
                    >
                      {Object.entries(securityLevels).map(([key, level]) => (
                        <MenuItem key={key} value={key}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <SecurityLevelChip level={key} label={level.label} size="small" />
                            <Typography variant="body2">{level.description}</Typography>
                          </Box>
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Selected Security Level: {securityLevels[securityLevel]?.label}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {securityLevels[securityLevel]?.description}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      <strong>Threshold:</strong> {securityLevels[securityLevel]?.threshold}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Algorithms:</strong> {securityLevels[securityLevel]?.algorithms.join(', ')}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <StyledCard>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Face Images ({faceImages.length}/{MAX_FACE_IMAGES})
                      </Typography>
                      {faceImages.length < MAX_FACE_IMAGES && (
                        <Box sx={{ textAlign: 'center', mb: 2 }}>
                          <video
                            ref={videoRef}
                            width="320"
                            height="240"
                            autoPlay
                            style={{ borderRadius: 8, border: "1px solid #ccc" }}
                          />
                          <canvas
                            ref={canvasRef}
                            width="320"
                            height="240"
                            style={{ display: "none" }}
                          />
                          <Typography variant="body2" sx={{ mt: 1, mb: 1 }}>
                            {faceCaptureInstructions[faceImages.length]}
                          </Typography>
                          <Box>
                            <Button
                              variant="contained"
                              onClick={startCamera}
                              sx={{ mr: 1 }}
                              startIcon={<CameraIcon />}
                            >
                              Start Camera
                            </Button>
                            <Button
                              variant="contained"
                              color="secondary"
                              onClick={captureImage}
                              disabled={!videoRef.current?.srcObject}
                              startIcon={<CameraIcon />}
                            >
                              Capture
                            </Button>
                          </Box>
                        </Box>
                      )}
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
                        {faceImages.map((img, idx) => (
                          <Box key={idx} sx={{ position: 'relative' }}>
                            <img
                              src={URL.createObjectURL(img)}
                              alt={`face${idx}`}
                              style={{ width: 80, height: 80, borderRadius: 4, border: '1px solid #aaa' }}
                            />
                            <IconButton
                              size="small"
                              sx={{ position: 'absolute', top: -8, right: -8, bgcolor: 'error.main' }}
                              onClick={() => setFaceImages(prev => prev.filter((_, i) => i !== idx))}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Box>
                        ))}
                      </Box>
                      <PulsingProgress
                        variant="determinate"
                        value={(faceImages.length / MAX_FACE_IMAGES) * 100}
                        sx={{ mt: 2 }}
                      />
                    </CardContent>
                  </StyledCard>
                </Grid>
                <Grid item xs={12} md={6}>
                  <StyledCard>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Fingerprint
                      </Typography>
                      <Button
                        variant="contained"
                        component="label"
                        fullWidth
                        sx={{ mb: 2 }}
                        startIcon={<UploadFileIcon />}
                      >
                        Upload Fingerprint
                        <input
                          type="file"
                          hidden
                          accept=".bmp,.png,.jpg,.jpeg"
                          onChange={(e) => setFpFile(e.target.files[0])}
                        />
                      </Button>
                      {fpFile && (
                        <Box sx={{ textAlign: 'center' }}>
                          <Typography variant="body2" gutterBottom>
                            Selected: {fpFile.name}
                          </Typography>
                          <img
                            src={URL.createObjectURL(fpFile)}
                            alt="fingerprint"
                            style={{ width: '100%', maxWidth: 200, borderRadius: 8 }}
                          />
                        </Box>
                      )}
                    </CardContent>
                  </StyledCard>
                </Grid>
              </Grid>

              <Box sx={{ mt: 3, textAlign: 'center' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleRegister}
                  disabled={loading || faceImages.length < MAX_FACE_IMAGES || !fpFile || !username}
                  startIcon={loading ? <CircularProgress size={20} /> : <PersonAddIcon />}
                  sx={{ minWidth: 200 }}
                >
                  {loading ? 'Registering...' : 'Register User'}
                </Button>
              </Box>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <Typography variant="h6" gutterBottom>
                System Settings
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={showAlgorithmDetails}
                    onChange={(e) => setShowAlgorithmDetails(e.target.checked)}
                  />
                }
                label="Show Algorithm Details"
              />
              
              {systemStatus && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    System Information
                  </Typography>
                  <TableContainer component={Paper}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Property</TableCell>
                          <TableCell>Value</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>System Status</TableCell>
                          <TableCell>
                            <Chip label={systemStatus.status} color="success" size="small" />
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Active Users</TableCell>
                          <TableCell>{systemStatus.user_count}</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>DeepFace Available</TableCell>
                          <TableCell>
                            <Chip 
                              label={systemStatus.deepface_available ? 'Yes' : 'No'} 
                              color={systemStatus.deepface_available ? 'success' : 'error'} 
                              size="small" 
                            />
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Face Algorithms</TableCell>
                          <TableCell>
                            {systemStatus.algorithms_available?.face?.map(alg => (
                              <Chip key={alg} label={alg} size="small" sx={{ mr: 0.5 }} />
                            ))}
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Fingerprint Algorithms</TableCell>
                          <TableCell>
                            {systemStatus.algorithms_available?.fingerprint?.map(alg => (
                              <Chip key={alg} label={alg} size="small" sx={{ mr: 0.5 }} />
                            ))}
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>
              )}
            </TabPanel>
          </CardContent>
        </StyledCard>
      </Container>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
}