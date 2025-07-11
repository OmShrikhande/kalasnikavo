import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Grid,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Speed as SpeedIcon,
  Person as PersonIcon,
  Security as SecurityIcon,
  Schedule as ScheduleIcon,
  LocationOn as LocationIcon,
  DeviceHub as DeviceIcon,
  Fingerprint as FingerprintIcon,
  Face as FaceIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon
} from '@mui/icons-material';

export default function Analytics({ authAttempts, performanceMetrics, userBehavior }) {
  const [timeRange, setTimeRange] = useState('7d');
  const [analyticsData, setAnalyticsData] = useState({
    authSuccessRate: 0,
    averageAuthTime: 0,
    peakUsageHours: [],
    topFailureReasons: [],
    deviceTypes: {},
    locationStats: {},
    biometricAccuracy: { face: 0, fingerprint: 0 }
  });

  useEffect(() => {
    calculateAnalytics();
  }, [authAttempts, performanceMetrics, userBehavior, timeRange]);

  const calculateAnalytics = () => {
    // Simulate analytics calculations
    const totalAttempts = authAttempts?.length || 100;
    const successfulAttempts = Math.floor(totalAttempts * 0.85);
    
    setAnalyticsData({
      authSuccessRate: (successfulAttempts / totalAttempts) * 100,
      averageAuthTime: performanceMetrics?.totalAuthTime || 2.3,
      peakUsageHours: ['09:00', '14:00', '18:00'],
      topFailureReasons: [
        { reason: 'Poor image quality', count: 15 },
        { reason: 'Face not detected', count: 12 },
        { reason: 'Fingerprint mismatch', count: 8 },
        { reason: 'Multiple faces detected', count: 5 }
      ],
      deviceTypes: {
        'Desktop': 45,
        'Mobile': 35,
        'Tablet': 20
      },
      locationStats: {
        'Office': 60,
        'Home': 30,
        'Other': 10
      },
      biometricAccuracy: {
        face: performanceMetrics?.faceConfidence || 87.5,
        fingerprint: 92.3
      }
    });
  };

  const MetricCard = ({ title, value, subtitle, icon: Icon, color = 'primary', trend }) => (
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
            {subtitle && (
              <Typography variant="body2" color="textSecondary">
                {subtitle}
              </Typography>
            )}
            {trend && (
              <Box display="flex" alignItems="center" mt={1}>
                <TrendingUpIcon 
                  sx={{ 
                    fontSize: 16, 
                    color: trend > 0 ? 'success.main' : 'error.main',
                    mr: 0.5 
                  }} 
                />
                <Typography 
                  variant="caption" 
                  color={trend > 0 ? 'success.main' : 'error.main'}
                >
                  {trend > 0 ? '+' : ''}{trend}%
                </Typography>
              </Box>
            )}
          </Box>
          <Avatar sx={{ bgcolor: `${color}.main`, width: 56, height: 56 }}>
            <Icon />
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  const PerformanceChart = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Authentication Performance
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="textSecondary">
            Average Response Time: {analyticsData.averageAuthTime}s
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={Math.min((3 - analyticsData.averageAuthTime) / 3 * 100, 100)}
            sx={{ mt: 1, height: 8, borderRadius: 4 }}
          />
        </Box>
        
        <Typography variant="body2" gutterBottom>
          Biometric Accuracy
        </Typography>
        <Box sx={{ mb: 1 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="body2">Face Recognition</Typography>
            <Typography variant="body2">{analyticsData.biometricAccuracy.face.toFixed(1)}%</Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={analyticsData.biometricAccuracy.face}
            color="primary"
            sx={{ height: 6, borderRadius: 3 }}
          />
        </Box>
        <Box>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="body2">Fingerprint Recognition</Typography>
            <Typography variant="body2">{analyticsData.biometricAccuracy.fingerprint.toFixed(1)}%</Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={analyticsData.biometricAccuracy.fingerprint}
            color="secondary"
            sx={{ height: 6, borderRadius: 3 }}
          />
        </Box>
      </CardContent>
    </Card>
  );

  const FailureAnalysis = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Top Failure Reasons
        </Typography>
        <List>
          {analyticsData.topFailureReasons.map((item, index) => (
            <ListItem key={index}>
              <ListItemIcon>
                <Avatar sx={{ bgcolor: 'error.light', width: 32, height: 32 }}>
                  {index + 1}
                </Avatar>
              </ListItemIcon>
              <ListItemText
                primary={item.reason}
                secondary={`${item.count} occurrences`}
              />
              <Chip 
                label={`${((item.count / 40) * 100).toFixed(0)}%`}
                size="small"
                color="error"
                variant="outlined"
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );

  const UsagePatterns = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Usage Patterns
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Peak Usage Hours
          </Typography>
          <Box display="flex" gap={1} flexWrap="wrap">
            {analyticsData.peakUsageHours.map((hour, index) => (
              <Chip 
                key={index}
                label={hour}
                color="primary"
                variant="outlined"
                icon={<ScheduleIcon />}
              />
            ))}
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Device Distribution
          </Typography>
          {Object.entries(analyticsData.deviceTypes).map(([device, percentage]) => (
            <Box key={device} sx={{ mb: 1 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="body2">{device}</Typography>
                <Typography variant="body2">{percentage}%</Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={percentage}
                sx={{ height: 6, borderRadius: 3 }}
              />
            </Box>
          ))}
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box>
          <Typography variant="subtitle2" gutterBottom>
            Access Locations
          </Typography>
          {Object.entries(analyticsData.locationStats).map(([location, percentage]) => (
            <Box key={location} sx={{ mb: 1 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="body2">{location}</Typography>
                <Typography variant="body2">{percentage}%</Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={percentage}
                color="secondary"
                sx={{ height: 6, borderRadius: 3 }}
              />
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );

  const UserBehaviorAnalysis = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          User Behavior Analysis
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Box textAlign="center">
              <Typography variant="h4" color="primary">
                {userBehavior.mouseMovements || 1247}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Mouse Movements
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box textAlign="center">
              <Typography variant="h4" color="secondary">
                {userBehavior.keystrokes || 89}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Keystrokes
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box textAlign="center">
              <Typography variant="h4" color="success.main">
                {userBehavior.clickEvents || 34}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Click Events
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box textAlign="center">
              <Typography variant="h4" color="warning.main">
                {userBehavior.scrollEvents || 156}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Scroll Events
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Analytics Dashboard
        </Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Time Range</InputLabel>
          <Select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            label="Time Range"
          >
            <MenuItem value="1d">Last 24 Hours</MenuItem>
            <MenuItem value="7d">Last 7 Days</MenuItem>
            <MenuItem value="30d">Last 30 Days</MenuItem>
            <MenuItem value="90d">Last 90 Days</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Success Rate"
            value={`${analyticsData.authSuccessRate.toFixed(1)}%`}
            icon={CheckCircleIcon}
            color="success"
            trend={2.3}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Avg Auth Time"
            value={`${analyticsData.averageAuthTime}s`}
            icon={SpeedIcon}
            color="primary"
            trend={-5.2}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Face Accuracy"
            value={`${analyticsData.biometricAccuracy.face.toFixed(1)}%`}
            icon={FaceIcon}
            color="info"
            trend={1.8}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Fingerprint Accuracy"
            value={`${analyticsData.biometricAccuracy.fingerprint.toFixed(1)}%`}
            icon={FingerprintIcon}
            color="secondary"
            trend={0.9}
          />
        </Grid>

        {/* Performance Chart */}
        <Grid item xs={12} md={6}>
          <PerformanceChart />
        </Grid>

        {/* Failure Analysis */}
        <Grid item xs={12} md={6}>
          <FailureAnalysis />
        </Grid>

        {/* Usage Patterns */}
        <Grid item xs={12} md={6}>
          <UsagePatterns />
        </Grid>

        {/* User Behavior */}
        <Grid item xs={12} md={6}>
          <UserBehaviorAnalysis />
        </Grid>
      </Grid>
    </Container>
  );
}