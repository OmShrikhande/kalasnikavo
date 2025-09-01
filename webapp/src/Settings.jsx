import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Switch,
  FormControlLabel,
  Slider,
  Box,
  Divider,
  Card,
  CardContent,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  TextField,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Palette as PaletteIcon,
  Speed as SpeedIcon,
  VolumeUp as VolumeUpIcon,
  Brightness4 as Brightness4Icon,
  Language as LanguageIcon,
  Storage as StorageIcon,
  Backup as BackupIcon,
  RestoreFromTrash as RestoreIcon,
  ExpandMore as ExpandMoreIcon,
  Save as SaveIcon,
  RestartAlt as RestartAltIcon
} from '@mui/icons-material';

const SECURITY_LEVELS = {
  LOW: { name: 'Basic', threshold: 0.6 },
  MEDIUM: { name: 'Standard', threshold: 0.75 },
  HIGH: { name: 'Enhanced', threshold: 0.85 },
  MAXIMUM: { name: 'Maximum', threshold: 0.95 }
};

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'zh', name: '中文' },
  { code: 'ja', name: '日本語' }
];

const THEMES = [
  { id: 'light', name: 'Light' },
  { id: 'dark', name: 'Dark' },
  { id: 'auto', name: 'Auto (System)' }
];

import axios from 'axios';

export default function Settings({ open, onClose, settings, onSettingsChange, username }) {
  const [localSettings, setLocalSettings] = useState(settings);
  const [hasChanges, setHasChanges] = useState(false);

  const handleSettingChange = (key, value) => {
    setLocalSettings(prev => ({
      ...prev,
      [key]: value
    }));
    setHasChanges(true);
  };

  const handleSave = () => {
    onSettingsChange(localSettings);
    // persist to backend
    axios.put('/api/user/settings', { username, settings: localSettings })
      .then(() => {
        setHasChanges(false);
        onClose();
      })
      .catch(() => {
        setHasChanges(false);
        onClose();
      });
  };

  const handleReset = () => {
    setLocalSettings(settings);
    setHasChanges(false);
  };

  const SecuritySettings = () => (
    <Accordion defaultExpanded>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box display="flex" alignItems="center" gap={1}>
          <SecurityIcon />
          <Typography variant="h6">Security Settings</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography gutterBottom>Security Level</Typography>
            <Slider
              value={Object.keys(SECURITY_LEVELS).indexOf(localSettings.securityLevel)}
              onChange={(e, value) => handleSettingChange('securityLevel', Object.keys(SECURITY_LEVELS)[value])}
              step={1}
              marks={Object.keys(SECURITY_LEVELS).map((level, index) => ({
                value: index,
                label: SECURITY_LEVELS[level].name
              }))}
              max={Object.keys(SECURITY_LEVELS).length - 1}
              valueLabelDisplay="off"
            />
            <Typography variant="body2" color="textSecondary">
              Current: {SECURITY_LEVELS[localSettings.securityLevel]?.name} 
              (Threshold: {(SECURITY_LEVELS[localSettings.securityLevel]?.threshold * 100).toFixed(0)}%)
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.livenessDetection}
                  onChange={(e) => handleSettingChange('livenessDetection', e.target.checked)}
                />
              }
              label="Liveness Detection"
            />
            <Typography variant="body2" color="textSecondary">
              Prevents spoofing attacks using photos or videos
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.multiFactorEnabled}
                  onChange={(e) => handleSettingChange('multiFactorEnabled', e.target.checked)}
                />
              }
              label="Multi-Factor Authentication"
            />
            <Typography variant="body2" color="textSecondary">
              Requires additional verification methods
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Typography gutterBottom>Session Timeout (minutes)</Typography>
            <Slider
              value={localSettings.sessionTimeout}
              onChange={(e, value) => handleSettingChange('sessionTimeout', value)}
              min={5}
              max={120}
              step={5}
              marks={[
                { value: 5, label: '5m' },
                { value: 30, label: '30m' },
                { value: 60, label: '1h' },
                { value: 120, label: '2h' }
              ]}
              valueLabelDisplay="auto"
            />
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );

  const BiometricSettings = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box display="flex" alignItems="center" gap={1}>
          <SecurityIcon />
          <Typography variant="h6">Biometric Settings</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.voiceRecognition}
                  onChange={(e) => handleSettingChange('voiceRecognition', e.target.checked)}
                />
              }
              label="Voice Commands"
            />
            <Typography variant="body2" color="textSecondary">
              Enable voice control for authentication
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.behaviorAnalysis}
                  onChange={(e) => handleSettingChange('behaviorAnalysis', e.target.checked)}
                />
              }
              label="Behavioral Analysis"
            />
            <Typography variant="body2" color="textSecondary">
              Monitor user behavior patterns for security
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Alert severity="info">
              Biometric data is processed locally and encrypted before storage. 
              No raw biometric data is transmitted or stored on external servers.
            </Alert>
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );

  const AppearanceSettings = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box display="flex" alignItems="center" gap={1}>
          <PaletteIcon />
          <Typography variant="h6">Appearance</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.darkMode}
                  onChange={(e) => handleSettingChange('darkMode', e.target.checked)}
                />
              }
              label="Dark Mode"
            />
            <Typography variant="body2" color="textSecondary">
              Use dark theme for better visibility in low light
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={localSettings.language || 'en'}
                onChange={(e) => handleSettingChange('language', e.target.value)}
                label="Language"
              >
                {LANGUAGES.map((lang) => (
                  <MenuItem key={lang.code} value={lang.code}>
                    {lang.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Typography gutterBottom>UI Scale</Typography>
            <Slider
              value={localSettings.uiScale || 100}
              onChange={(e, value) => handleSettingChange('uiScale', value)}
              min={75}
              max={150}
              step={25}
              marks={[
                { value: 75, label: '75%' },
                { value: 100, label: '100%' },
                { value: 125, label: '125%' },
                { value: 150, label: '150%' }
              ]}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `${value}%`}
            />
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );

  const NotificationSettings = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box display="flex" alignItems="center" gap={1}>
          <NotificationsIcon />
          <Typography variant="h6">Notifications</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <List>
          <ListItem>
            <ListItemText
              primary="Security Alerts"
              secondary="Get notified about security events"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={localSettings.securityAlerts !== false}
                onChange={(e) => handleSettingChange('securityAlerts', e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>

          <ListItem>
            <ListItemText
              primary="Login Notifications"
              secondary="Notify on successful logins"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={localSettings.loginNotifications !== false}
                onChange={(e) => handleSettingChange('loginNotifications', e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>

          <ListItem>
            <ListItemText
              primary="System Updates"
              secondary="Notify about system updates"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={localSettings.systemUpdates !== false}
                onChange={(e) => handleSettingChange('systemUpdates', e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>

          <ListItem>
            <ListItemText
              primary="Sound Notifications"
              secondary="Play sounds for notifications"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={localSettings.soundNotifications !== false}
                onChange={(e) => handleSettingChange('soundNotifications', e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>
        </List>
      </AccordionDetails>
    </Accordion>
  );

  const AdvancedSettings = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box display="flex" alignItems="center" gap={1}>
          <SettingsIcon />
          <Typography variant="h6">Advanced</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Alert severity="warning">
              Advanced settings can affect system performance and security. 
              Change these settings only if you understand their implications.
            </Alert>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.debugMode || false}
                  onChange={(e) => handleSettingChange('debugMode', e.target.checked)}
                />
              }
              label="Debug Mode"
            />
            <Typography variant="body2" color="textSecondary">
              Enable detailed logging for troubleshooting
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={localSettings.offlineMode || false}
                  onChange={(e) => handleSettingChange('offlineMode', e.target.checked)}
                />
              }
              label="Offline Mode"
            />
            <Typography variant="body2" color="textSecondary">
              Allow authentication without internet connection
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Typography gutterBottom>Cache Size (MB)</Typography>
            <Slider
              value={localSettings.cacheSize || 100}
              onChange={(e, value) => handleSettingChange('cacheSize', value)}
              min={50}
              max={500}
              step={50}
              marks={[
                { value: 50, label: '50MB' },
                { value: 100, label: '100MB' },
                { value: 250, label: '250MB' },
                { value: 500, label: '500MB' }
              ]}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `${value}MB`}
            />
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { height: '80vh' }
      }}
    >
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          <SettingsIcon />
          <Typography variant="h5">Settings</Typography>
          {hasChanges && (
            <Chip label="Unsaved Changes" color="warning" size="small" />
          )}
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ mb: 2 }}>
          <SecuritySettings />
          <BiometricSettings />
          <AppearanceSettings />
          <NotificationSettings />
          <AdvancedSettings />
        </Box>
      </DialogContent>

      <DialogActions>
        <Button
          onClick={handleReset}
          disabled={!hasChanges}
          startIcon={<RestartAltIcon />}
        >
          Reset
        </Button>
        <Button onClick={onClose}>
          Cancel
        </Button>
        <Button
          onClick={handleSave}
          variant="contained"
          disabled={!hasChanges}
          startIcon={<SaveIcon />}
        >
          Save Settings
        </Button>
      </DialogActions>
    </Dialog>
  );
}