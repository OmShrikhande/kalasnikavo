import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Grid,
  Box,
  Avatar,
  Button,
  TextField,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  IconButton,
  Badge,
  Tooltip
} from '@mui/material';
import {
  Person as PersonIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  Security as SecurityIcon,
  Fingerprint as FingerprintIcon,
  Face as FaceIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  Shield as ShieldIcon,
  Verified as VerifiedIcon,
  Schedule as ScheduleIcon,
  LocationOn as LocationIcon,
  DeviceHub as DeviceIcon,
  History as HistoryIcon,
  Settings as SettingsIcon,
  Lock as LockIcon,
  Key as KeyIcon
} from '@mui/icons-material';

const SECURITY_LEVELS = {
  LOW: { name: 'Basic', color: 'warning', description: 'Standard security' },
  MEDIUM: { name: 'Standard', color: 'info', description: 'Enhanced security' },
  HIGH: { name: 'Enhanced', color: 'success', description: 'High security' },
  MAXIMUM: { name: 'Maximum', color: 'error', description: 'Maximum security' }
};

export default function UserProfile({ 
  username, 
  email, 
  phoneNumber, 
  securityLevel, 
  biometricQuality 
}) {
  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState({
    email: email || '',
    phoneNumber: phoneNumber || ''
  });
  const [changePasswordOpen, setChangePasswordOpen] = useState(false);
  const [biometricUpdateOpen, setBiometricUpdateOpen] = useState(false);

  const userStats = {
    joinDate: '2024-01-15',
    lastLogin: new Date().toISOString(),
    totalLogins: 247,
    successRate: 96.8,
    averageSessionTime: '45 min',
    preferredDevice: 'Desktop',
    registeredBiometrics: ['Face', 'Fingerprint']
  };

  const handleSaveProfile = () => {
    // Save profile changes
    setEditMode(false);
    // API call would go here
  };

  const ProfileHeader = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box display="flex" alignItems="center" gap={3}>
          <Badge
            overlap="circular"
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            badgeContent={
              <Avatar sx={{ bgcolor: 'success.main', width: 24, height: 24 }}>
                <VerifiedIcon sx={{ fontSize: 16 }} />
              </Avatar>
            }
          >
            <Avatar
              sx={{ 
                width: 80, 
                height: 80, 
                bgcolor: 'primary.main',
                fontSize: '2rem'
              }}
            >
              {username?.[0]?.toUpperCase()}
            </Avatar>
          </Badge>
          
          <Box flexGrow={1}>
            <Typography variant="h4" gutterBottom>
              {username}
            </Typography>
            <Box display="flex" alignItems="center" gap={2} mb={1}>
              <Chip 
                label={`Security: ${SECURITY_LEVELS[securityLevel]?.name}`}
                color={SECURITY_LEVELS[securityLevel]?.color}
                icon={<ShieldIcon />}
              />
              <Chip 
                label="Verified Account"
                color="success"
                icon={<VerifiedIcon />}
              />
            </Box>
            <Typography variant="body2" color="textSecondary">
              Member since {new Date(userStats.joinDate).toLocaleDateString()}
            </Typography>
          </Box>

          <IconButton 
            onClick={() => setEditMode(!editMode)}
            color="primary"
          >
            {editMode ? <CancelIcon /> : <EditIcon />}
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );

  const ContactInformation = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Contact Information
        </Typography>
        
        <List>
          <ListItem>
            <ListItemIcon>
              <PersonIcon />
            </ListItemIcon>
            <ListItemText
              primary="Username"
              secondary={username}
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <EmailIcon />
            </ListItemIcon>
            <ListItemText
              primary="Email"
              secondary={
                editMode ? (
                  <TextField
                    value={editData.email}
                    onChange={(e) => setEditData({...editData, email: e.target.value})}
                    size="small"
                    fullWidth
                    sx={{ mt: 1 }}
                  />
                ) : (
                  email || 'Not provided'
                )
              }
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <PhoneIcon />
            </ListItemIcon>
            <ListItemText
              primary="Phone Number"
              secondary={
                editMode ? (
                  <TextField
                    value={editData.phoneNumber}
                    onChange={(e) => setEditData({...editData, phoneNumber: e.target.value})}
                    size="small"
                    fullWidth
                    sx={{ mt: 1 }}
                  />
                ) : (
                  phoneNumber || 'Not provided'
                )
              }
            />
          </ListItem>
        </List>

        {editMode && (
          <Box display="flex" gap={2} mt={2}>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={handleSaveProfile}
            >
              Save Changes
            </Button>
            <Button
              variant="outlined"
              onClick={() => setEditMode(false)}
            >
              Cancel
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const BiometricStatus = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Biometric Authentication
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={1}>
                <FaceIcon color="primary" />
                <Typography variant="subtitle2">Face Recognition</Typography>
                <Chip label="Active" color="success" size="small" />
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={(biometricQuality?.face || 0.85) * 100}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="textSecondary">
                Quality: {((biometricQuality?.face || 0.85) * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={1}>
                <FingerprintIcon color="secondary" />
                <Typography variant="subtitle2">Fingerprint</Typography>
                <Chip label="Active" color="success" size="small" />
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={(biometricQuality?.fingerprint || 0.92) * 100}
                color="secondary"
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="textSecondary">
                Quality: {((biometricQuality?.fingerprint || 0.92) * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>
        </Grid>

        <Box display="flex" gap={2} mt={2}>
          <Button
            variant="outlined"
            startIcon={<FaceIcon />}
            onClick={() => setBiometricUpdateOpen(true)}
          >
            Update Face Data
          </Button>
          <Button
            variant="outlined"
            startIcon={<FingerprintIcon />}
            onClick={() => setBiometricUpdateOpen(true)}
          >
            Update Fingerprint
          </Button>
        </Box>
      </CardContent>
    </Card>
  );

  const AccountStatistics = () => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Account Statistics
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="primary">
                {userStats.totalLogins}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total Logins
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="success.main">
                {userStats.successRate}%
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Success Rate
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="info.main">
                {userStats.averageSessionTime}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Avg Session
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={6} md={3}>
            <Box textAlign="center">
              <Typography variant="h4" color="secondary.main">
                {userStats.preferredDevice}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Preferred Device
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const SecuritySettings = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Security Settings
        </Typography>
        
        <List>
          <ListItem button onClick={() => setChangePasswordOpen(true)}>
            <ListItemIcon>
              <KeyIcon />
            </ListItemIcon>
            <ListItemText
              primary="Change Password"
              secondary="Update your account password"
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <ShieldIcon />
            </ListItemIcon>
            <ListItemText
              primary="Security Level"
              secondary={SECURITY_LEVELS[securityLevel]?.description}
            />
            <Chip 
              label={SECURITY_LEVELS[securityLevel]?.name}
              color={SECURITY_LEVELS[securityLevel]?.color}
              size="small"
            />
          </ListItem>
          
          <ListItem>
            <ListItemIcon>
              <ScheduleIcon />
            </ListItemIcon>
            <ListItemText
              primary="Last Login"
              secondary={new Date(userStats.lastLogin).toLocaleString()}
            />
          </ListItem>
        </List>
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        User Profile
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <ProfileHeader />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <ContactInformation />
          <BiometricStatus />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <AccountStatistics />
          <SecuritySettings />
        </Grid>
      </Grid>

      {/* Change Password Dialog */}
      <Dialog
        open={changePasswordOpen}
        onClose={() => setChangePasswordOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Change Password</DialogTitle>
        <DialogContent>
          <TextField
            label="Current Password"
            type="password"
            fullWidth
            margin="normal"
          />
          <TextField
            label="New Password"
            type="password"
            fullWidth
            margin="normal"
          />
          <TextField
            label="Confirm New Password"
            type="password"
            fullWidth
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setChangePasswordOpen(false)}>
            Cancel
          </Button>
          <Button variant="contained">
            Update Password
          </Button>
        </DialogActions>
      </Dialog>

      {/* Biometric Update Dialog */}
      <Dialog
        open={biometricUpdateOpen}
        onClose={() => setBiometricUpdateOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Update Biometric Data</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            Updating biometric data will require re-enrollment. This process helps maintain security and accuracy.
          </Alert>
          <Typography variant="body2" color="textSecondary">
            Choose which biometric data you'd like to update:
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBiometricUpdateOpen(false)}>
            Cancel
          </Button>
          <Button variant="outlined" startIcon={<FaceIcon />}>
            Update Face
          </Button>
          <Button variant="outlined" startIcon={<FingerprintIcon />}>
            Update Fingerprint
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}