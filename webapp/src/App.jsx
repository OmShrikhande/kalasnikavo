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
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  ThemeProvider,
  CssBaseline,
  useMediaQuery,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Backdrop,
  Modal,
  Tab,
  Tabs,
  Accordion,
  AccordionSummary,
  AccordionDetails,
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
  Help as HelpIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Camera as CameraIcon,
  CameraAlt as CameraAltIcon,
  Refresh as RefreshIcon,
  Save as SaveIcon,
  Share as ShareIcon,
  Download as DownloadIcon,
  CloudUpload as CloudUploadIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  PersonAdd as PersonAddIcon,
  Login as LoginIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
  PlayArrow as PlayArrowIcon,
  Stop as StopIcon,
  Pause as PauseIcon,
  VolumeUp as VolumeUpIcon,
  VolumeOff as VolumeOffIcon,
  Brightness4 as Brightness4Icon,
  Brightness7 as Brightness7Icon,
  Fullscreen as FullscreenIcon,
  FullscreenExit as FullscreenExitIcon,
  QrCode as QrCodeIcon,
  QrCodeScanner as QrCodeScannerIcon,
  Shield as ShieldIcon,
  Speed as SpeedIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon
} from "@mui/icons-material";
import axios from "axios";
import Dashboard from "./Dashboard";
import theme from "./theme";

// Set axios base URL
axios.defaults.baseURL = 'http://localhost:5000';

const steps = ["Capture Face Images", "Fingerprint Recognition"];
const MAX_FACE_IMAGES = 5;

export default function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [username, setUsername] = useState("");
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
  const [captureStep, setCaptureStep] = useState(0);
  const [dashboard, setDashboard] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [docUploadLoading, setDocUploadLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const startCamera = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
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
      ctx.drawImage(videoRef.current, 0, 0, 320, 240);
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
    // Only send the first face image as 'face' for simple backend
    form.append("face", faceImages[0]);
    form.append("fingerprint", fpFile);
    try {
      await axios.post("/api/register", form);
      setSnackbar({
        open: true,
        message: "Registration successful!",
        severity: "success",
      });
      setRegisterMode(false);
      resetRegistration();
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
      await axios.post("/api/auth/face", form);
      setActiveStep(1);
      setSnackbar({
        open: true,
        message: "Face recognized! Please provide fingerprint.",
        severity: "success",
      });
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Face not recognized",
        severity: "error",
      });
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
      await axios.post("/api/auth/fingerprint", form);
      setSnackbar({
        open: true,
        message: "Access granted!",
        severity: "success",
      });
      setActiveStep(0);
      setFaceImages([]);
      setFpFile(null);
      setDashboard(true);
      // Remove or comment out the next line for simple backend:
      // fetchDocuments();
    } catch (e) {
      setSnackbar({
        open: true,
        message: e.response?.data?.error || "Fingerprint not recognized",
        severity: "error",
      });
    }
    setFpAuthLoading(false);
  };

  const fetchDocuments = async () => {
    try {
      const res = await axios.get(
        `/api/user/docs?username=${encodeURIComponent(username)}`
      );
      setDocuments(res.data.docs || []);
    } catch {
      setDocuments([]);
    }
  };

  const handleLogout = () => {
    setDashboard(false);
    setUsername("");
    setDocuments([]);
    setActiveStep(0);
    setRegisterMode(false);
  };

  const faceCaptureInstructions = [
    "Look straight at the camera.",
    "Turn your face slightly to the left.",
    "Turn your face slightly to the right.",
    "Look up slightly.",
    "Look down slightly.",
  ];

  if (dashboard) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Dashboard username={username} onLogout={handleLogout} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="sm" sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" align="center" gutterBottom>
            Dual Biometric Authentication
          </Typography>
        <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Box sx={{ mb: 2 }}>
          <TextField
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
            sx={{ mb: 2 }}
          />
          <Button
            onClick={() => {
              setRegisterMode(!registerMode);
              resetRegistration();
            }}
            sx={{ mb: 2 }}
          >
            {registerMode ? "Back to Login" : "Register New User"}
          </Button>
        </Box>
        {registerMode ? (
          <Box>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>
              Step 1: Capture Face Images
            </Typography>
            {faceImages.length < MAX_FACE_IMAGES && (
              <Box sx={{ mb: 2 }}>
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
                <Typography sx={{ mt: 1, mb: 1 }}>
                  {faceCaptureInstructions[faceImages.length]}
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={startCamera}
                  sx={{ mr: 1 }}
                >
                  Start Camera
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={captureImage}
                  sx={{ mr: 1 }}
                  disabled={
                    !videoRef.current || !videoRef.current.srcObject
                  }
                >
                  Capture
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={stopCamera}
                >
                  Stop Camera
                </Button>
              </Box>
            )}
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2">
                Captured Images: {faceImages.length}/{MAX_FACE_IMAGES}
              </Typography>
              <Box sx={{ display: "flex", gap: 1, mt: 1 }}>
                {faceImages.map((img, idx) => (
                  <img
                    key={idx}
                    src={URL.createObjectURL(img)}
                    alt={`face${idx}`}
                    width={48}
                    height={48}
                    style={{
                      borderRadius: 4,
                      border: "1px solid #aaa",
                    }}
                  />
                ))}
              </Box>
              <LinearProgress
                variant="determinate"
                value={(faceImages.length * 100) / MAX_FACE_IMAGES}
                sx={{ mt: 1 }}
              />
            </Box>
            <Typography variant="subtitle1" sx={{ mb: 1 }}>
              Step 2: Upload Fingerprint
            </Typography>
            <Button
              variant="contained"
              component="label"
              fullWidth
              sx={{ mb: 2 }}
            >
              Upload Fingerprint
              <input
                type="file"
                hidden
                accept=".bmp"
                onChange={(e) => setFpFile(e.target.files[0])}
              />
            </Button>
            {fpFile && (
              <Typography variant="body2" sx={{ mb: 2 }}>
                Selected: {fpFile.name}
              </Typography>
            )}
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handleRegister}
              disabled={
                loading ||
                faceImages.length < MAX_FACE_IMAGES ||
                !fpFile
              }
            >
              {loading ? (
                <CircularProgress size={24} />
              ) : (
                "Register"
              )}
            </Button>
          </Box>
        ) : (
          <Box>
            {activeStep === 0 && (
              <>
                <Typography variant="subtitle1" sx={{ mb: 1 }}>
                  Capture Face Image for Login
                </Typography>
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
                <Button
                  variant="contained"
                  color="primary"
                  onClick={startCamera}
                  sx={{ mr: 1 }}
                >
                  Start Camera
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => {
                    if (videoRef.current && canvasRef.current) {
                      const ctx = canvasRef.current.getContext("2d");
                      ctx.drawImage(videoRef.current, 0, 0, 320, 240);
                      canvasRef.current.toBlob(
                        (blob) => {
                          setFaceImages([
                            new File([blob], "login_face.jpg", {
                              type: "image/jpeg",
                            }),
                          ]);
                        },
                        "image/jpeg",
                        0.95
                      );
                    }
                  }}
                  sx={{ mr: 1 }}
                  disabled={
                    !videoRef.current || !videoRef.current.srcObject
                  }
                >
                  Capture
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={stopCamera}
                >
                  Stop Camera
                </Button>
                <Box sx={{ mt: 2 }}>
                  {faceImages.length > 0 && (
                    <img
                      src={URL.createObjectURL(faceImages[0])}
                      alt="login_face"
                      width={96}
                      height={96}
                      style={{
                        borderRadius: 8,
                        border: "1px solid #aaa",
                      }}
                    />
                  )}
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={handleFaceAuth}
                  disabled={
                    faceAuthLoading || faceImages.length === 0
                  }
                >
                  {faceAuthLoading ? (
                    <CircularProgress size={24} />
                  ) : (
                    "Authenticate Face"
                  )}
                </Button>
              </>
            )}
            {activeStep === 1 && (
              <>
                <Button
                  variant="contained"
                  component="label"
                  fullWidth
                  sx={{ mb: 2 }}
                >
                  Upload Fingerprint
                  <input
                    type="file"
                    hidden
                    accept=".bmp"
                    onChange={(e) => setFpFile(e.target.files[0])}
                  />
                </Button>
                {fpFile && (
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Selected: {fpFile.name}
                  </Typography>
                )}
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  onClick={handleFpAuth}
                  disabled={fpAuthLoading || !fpFile}
                >
                  {fpAuthLoading ? (
                    <CircularProgress size={24} />
                  ) : (
                    "Authenticate Fingerprint"
                  )}
                </Button>
              </>
            )}
          </Box>
        )}
      </Paper>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} sx={{ width: "100%" }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
    </ThemeProvider>
  );
}
