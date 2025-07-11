import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Grid,
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Avatar,
  LinearProgress,
  Alert,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Badge,
  Switch,
  FormControlLabel,
  Slider,
  Divider
} from '@mui/material';
import {
  Security as SecurityIcon,
  Shield as ShieldIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Visibility as VisibilityIcon,
  Block as BlockIcon,
  VpnKey as VpnKeyIcon,
  Fingerprint as FingerprintIcon,
  Face as FaceIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

const SECURITY_LEVELS = {
  LOW: { name: 'Basic', color: 'warning', threshold: 0.6, description: 'Standard security with basic biometric verification' },
  MEDIUM: { name: 'Standard', color: 'info', threshold: 0.75, description: 'Enhanced security with improved accuracy' },
  HIGH: { name: 'Enhanced', color: 'success', threshold: 0.85, description: 'High security with advanced threat detection' },
  MAXIMUM: { name: 'Maximum', color: 'error', threshold: 0.95, description: 'Maximum security with military-grade protection' }
};

const THREAT_LEVELS = {
  LOW: { color: 'success', icon: CheckCircleIcon },
  MEDIUM: { color: 'warning', icon: WarningIcon },
  HIGH: { color: 'error', icon: ErrorIcon },
  CRITICAL: { color: 'error', icon: BlockIcon }
};

export default function SecurityCenter({ securityEvents, securityLevel, onSecurityLevelChange }) {
  const [threatLevel, setThreatLevel] = useState('LOW');
  const [activeThreats, setActiveThreats] = useState([]);
  const [securityMetrics, setSecurityMetrics] = useState({
    totalAttempts: 0,
    successfulAuth: 0,
    failedAttempts: 0,
    blockedAttempts: 0,
    averageResponseTime: 0
  });
  const [alertsEnabled, setAlertsEnabled] = useState(true);
  const [autoBlock, setAutoBlock] = useState(true);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    calculateSecurityMetrics();
    assessThreatLevel();
  }, [securityEvents]);

  const calculateSecurityMetrics = () => {
    if (!securityEvents.length) return;

    const total = securityEvents.length;
    const successful = securityEvents.filter(e => 
      e.type.includes('SUCCESS')).length;
    const failed = securityEvents.filter(e => 
      e.type.includes('FAILED')).length;
    const blocked = securityEvents.filter(e => 
      e.type.includes('BLOCKED')).length;

    setSecurityMetrics({
      totalAttempts: total,
      successfulAuth: successful,
      failedAttempts: failed,
      blockedAttempts: blocked,
      averageResponseTime: 1.2 // Simulated
    });
  };

  const assessThreatLevel = () => {
    const recentEvents = securityEvents.slice(0, 10);
    const failureRate = recentEvents.filter(e => 
      e.type.includes('FAILED')).length / Math.max(recentEvents.length, 1);

    if (failureRate > 0.7) {
      setThreatLevel('CRITICAL');
    } else if (failureRate > 0.5) {
      setThreatLevel('HIGH');
    } else if (failureRate > 0.3) {
      setThreatLevel('MEDIUM');
    } else {
      setThreatLevel('LOW');
    }
  };

  const SecurityMetricCard = ({ title, value, icon: Icon, color = 'primary' }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <Avatar sx={{ bgcolor: `${color}.main`, width: 56, height: 56 }}>
            <Icon />
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  const ThreatIndicator = () => {
    const threat = THREAT_LEVELS[threatLevel];
    const ThreatIcon = threat.icon;

    return (
      <Card sx={{ bgcolor: `${threat.color}.light`, color: `${threat.color}.contrastText` }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2}>
            <ThreatIcon sx={{ fontSize: 40 }} />
            <Box>
              <Typography variant="h6">
                Threat Level: {threatLevel}
              </Typography>
              <Typography variant="body2">
                Current security status assessment
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const SecurityEventsList = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Recent Security Events
        </Typography>
        <List>
          {securityEvents.slice(0, 10).map((event, index) => {
            const isSuccess = event.type.includes('SUCCESS');
            const isFailed = event.type.includes('FAILED');
            const isBlocked = event.type.includes('BLOCKED');
            
            let color = 'default';
            let icon = InfoIcon;
            
            if (isSuccess) {
              color = 'success';
              icon = CheckCircleIcon;
            } else if (isFailed) {
              color = 'warning';
              icon = WarningIcon;
            } else if (isBlocked) {
              color = 'error';
              icon = ErrorIcon;
            }

            const EventIcon = icon;

            return (
              <ListItem 
                key={event.id || index}
                button
                onClick={() => {
                  setSelectedEvent(event);
                  setDetailsOpen(true);
                }}
              >
                <ListItemIcon>
                  <EventIcon color={color} />
                </ListItemIcon>
                <ListItemText
                  primary={event.type.replace(/_/g, ' ')}
                  secondary={`${new Date(event.timestamp).toLocaleString()} - ${event.data?.username || 'Unknown'}`}
                />
                <Chip 
                  label={event.severity} 
                  color={color}
                  size="small"
                />
              </ListItem>
            );
          })}
        </List>
      </CardContent>
    </Card>
  );

  const SecuritySettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Security Configuration
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>Security Level</Typography>
          <Slider
            value={Object.keys(SECURITY_LEVELS).indexOf(securityLevel)}
            onChange={(e, value) => onSecurityLevelChange(Object.keys(SECURITY_LEVELS)[value])}
            step={1}
            marks={Object.keys(SECURITY_LEVELS).map((level, index) => ({
              value: index,
              label: SECURITY_LEVELS[level].name
            }))}
            max={Object.keys(SECURITY_LEVELS).length - 1}
            valueLabelDisplay="off"
          />
          <Typography variant="body2" color="textSecondary">
            {SECURITY_LEVELS[securityLevel].description}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        <FormControlLabel
          control={
            <Switch
              checked={alertsEnabled}
              onChange={(e) => setAlertsEnabled(e.target.checked)}
            />
          }
          label="Security Alerts"
        />
        
        <FormControlLabel
          control={
            <Switch
              checked={autoBlock}
              onChange={(e) => setAutoBlock(e.target.checked)}
            />
          }
          label="Auto-block Suspicious Activity"
        />
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Security Center
      </Typography>

      <Grid container spacing={3}>
        {/* Security Metrics */}
        <Grid item xs={12} sm={6} md={3}>
          <SecurityMetricCard
            title="Total Attempts"
            value={securityMetrics.totalAttempts}
            icon={SecurityIcon}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SecurityMetricCard
            title="Successful Auth"
            value={securityMetrics.successfulAuth}
            icon={CheckCircleIcon}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SecurityMetricCard
            title="Failed Attempts"
            value={securityMetrics.failedAttempts}
            icon={WarningIcon}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <SecurityMetricCard
            title="Blocked Attempts"
            value={securityMetrics.blockedAttempts}
            icon={BlockIcon}
            color="error"
          />
        </Grid>

        {/* Threat Level Indicator */}
        <Grid item xs={12}>
          <ThreatIndicator />
        </Grid>

        {/* Security Events and Settings */}
        <Grid item xs={12} md={8}>
          <SecurityEventsList />
        </Grid>
        <Grid item xs={12} md={4}>
          <SecuritySettings />
        </Grid>
      </Grid>

      {/* Event Details Dialog */}
      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Security Event Details</DialogTitle>
        <DialogContent>
          {selectedEvent && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {selectedEvent.type.replace(/_/g, ' ')}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                {new Date(selectedEvent.timestamp).toLocaleString()}
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="subtitle2">Severity</Typography>
                  <Chip label={selectedEvent.severity} color={
                    selectedEvent.severity === 'error' ? 'error' :
                    selectedEvent.severity === 'warning' ? 'warning' : 'success'
                  } />
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2">User</Typography>
                  <Typography>{selectedEvent.data?.username || 'N/A'}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2">Device Fingerprint</Typography>
                  <Typography variant="body2" sx={{ wordBreak: 'break-all' }}>
                    {selectedEvent.deviceFingerprint?.substring(0, 16)}...
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2">Location</Typography>
                  <Typography variant="body2">
                    {selectedEvent.location?.latitude ? 
                      `${selectedEvent.location.latitude.toFixed(4)}, ${selectedEvent.location.longitude.toFixed(4)}` : 
                      'N/A'
                    }
                  </Typography>
                </Grid>
              </Grid>

              {selectedEvent.data && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2">Additional Data</Typography>
                  <Paper sx={{ p: 2, bgcolor: 'grey.100', mt: 1 }}>
                    <pre style={{ margin: 0, fontSize: '0.875rem' }}>
                      {JSON.stringify(selectedEvent.data, null, 2)}
                    </pre>
                  </Paper>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}