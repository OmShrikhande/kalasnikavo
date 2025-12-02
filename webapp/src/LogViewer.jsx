import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Grid,
  Box,
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider,
  Alert,
  Skeleton,
  IconButton,
  Tooltip,
  Tabs,
  Tab,
  Pagination,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import {
  Timeline as TimelineIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  ContentCopy as CopyIcon,
  Refresh as RefreshIcon,
  VerifiedUser as VerifiedUserIcon,
  Security as SecurityIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  Key as KeyIcon
} from '@mui/icons-material';
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import TimelineOppositeContent from '@mui/lab/TimelineOppositeContent';

export default function LogViewer() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [viewMode, setViewMode] = useState(0);
  const [selectedLog, setSelectedLog] = useState(null);
  const [verificationDialog, setVerificationDialog] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);
  const [verifying, setVerifying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [copiedField, setCopiedField] = useState(null);

  useEffect(() => {
    fetchLogs();
  }, [page, perPage]);

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `/api/logs?page=${page}&per_page=${perPage}`
      );
      if (!response.ok) throw new Error('Failed to fetch logs');
      const data = await response.json();
      setLogs(data.logs || []);
      setTotalPages(data.pages || 1);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching logs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (logIndex) => {
    setVerifying(true);
    setVerificationResult(null);
    try {
      const response = await fetch(`/api/logs/${logIndex}/verify`);
      if (!response.ok) throw new Error('Failed to verify log');
      const data = await response.json();
      setVerificationResult(data);
      setVerificationDialog(true);
    } catch (err) {
      console.error('Error verifying log:', err);
      setVerificationResult({
        success: false,
        error: err.message
      });
      setVerificationDialog(true);
    } finally {
      setVerifying(false);
    }
  };

  const handleCopyToClipboard = (text, field) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setCopiedField(field);
    setTimeout(() => {
      setCopied(false);
      setCopiedField(null);
    }, 2000);
  };

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'ENROLL':
        return <CheckCircleIcon sx={{ color: '#4caf50' }} />;
      case 'AUTH_SUCCESS':
        return <CheckCircleIcon sx={{ color: '#2196f3' }} />;
      case 'AUTH_FAIL':
        return <ErrorIcon sx={{ color: '#f44336' }} />;
      case 'ADMIN_ACTION':
        return <SecurityIcon sx={{ color: '#ff9800' }} />;
      default:
        return <InfoIcon sx={{ color: '#9c27b0' }} />;
    }
  };

  const getEventColor = (eventType) => {
    switch (eventType) {
      case 'ENROLL':
        return '#4caf50';
      case 'AUTH_SUCCESS':
        return '#2196f3';
      case 'AUTH_FAIL':
        return '#f44336';
      case 'ADMIN_ACTION':
        return '#ff9800';
      default:
        return '#9c27b0';
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString();
  };

  const formatHash = (hash) => {
    if (!hash) return 'N/A';
    return `${hash.substring(0, 10)}...${hash.substring(hash.length - 8)}`;
  };

  const truncateHash = (hash, length = 32) => {
    if (!hash) return 'N/A';
    return hash.substring(0, length);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          <TimelineIcon />
          Blockchain Audit Logs
        </Typography>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={fetchLogs}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <Tabs value={viewMode} onChange={(e, newValue) => setViewMode(newValue)}>
          <Tab label="Table View" icon={<TimelineIcon />} iconPosition="start" />
          <Tab label="Timeline View" icon={<TimelineIcon />} iconPosition="start" />
        </Tabs>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} variant="rectangular" height={60} />
          ))}
        </Box>
      ) : logs.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="textSecondary">
            No logs available
          </Typography>
        </Paper>
      ) : (
        <>
          {viewMode === 0 ? (
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableCell sx={{ fontWeight: 'bold' }}>Event Type</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>User ID Hash</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Timestamp</TableCell>
                    <TableCell sx={{ fontWeight: 'bold' }}>Metadata Hash</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', textAlign: 'center' }}>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {logs.map((log, index) => (
                    <TableRow key={index} hover>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {getEventIcon(log.eventType)}
                          <Chip
                            label={log.eventType}
                            size="small"
                            sx={{
                              backgroundColor: getEventColor(log.eventType),
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Tooltip title={log.userIdHash}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <code>{formatHash(log.userIdHash)}</code>
                            <Tooltip title={copied && copiedField === `user_${index}` ? 'Copied!' : 'Copy'}>
                              <IconButton
                                size="small"
                                onClick={() => handleCopyToClipboard(log.userIdHash, `user_${index}`)}
                              >
                                <CopyIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{formatTimestamp(log.timestamp)}</TableCell>
                      <TableCell>
                        <Tooltip title={log.metaHash}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <code>{formatHash(log.metaHash)}</code>
                            <Tooltip title={copied && copiedField === `meta_${index}` ? 'Copied!' : 'Copy'}>
                              <IconButton
                                size="small"
                                onClick={() => handleCopyToClipboard(log.metaHash, `meta_${index}`)}
                              >
                                <CopyIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        </Tooltip>
                      </TableCell>
                      <TableCell sx={{ textAlign: 'center' }}>
                        <Tooltip title="Verify Integrity">
                          <Button
                            size="small"
                            variant="outlined"
                            startIcon={<VerifiedUserIcon />}
                            onClick={() => {
                              setSelectedLog(log);
                              handleVerify(log.index);
                            }}
                            disabled={verifying}
                          >
                            Verify
                          </Button>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          ) : (
            <Timeline position="alternate">
              {logs.map((log, index) => (
                <TimelineItem key={index}>
                  <TimelineOppositeContent color="textSecondary">
                    <Typography variant="body2">{formatTimestamp(log.timestamp)}</Typography>
                  </TimelineOppositeContent>
                  <TimelineSeparator>
                    <TimelineDot sx={{ backgroundColor: getEventColor(log.eventType) }}>
                      {getEventIcon(log.eventType)}
                    </TimelineDot>
                    {index < logs.length - 1 && <TimelineConnector />}
                  </TimelineSeparator>
                  <TimelineContent>
                    <Card sx={{ mb: 2 }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <Chip
                            label={log.eventType}
                            size="small"
                            sx={{
                              backgroundColor: getEventColor(log.eventType),
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>User ID Hash:</strong>
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                          <code style={{ fontSize: '12px', wordBreak: 'break-all' }}>
                            {truncateHash(log.userIdHash, 48)}
                          </code>
                          <Tooltip title={copied && copiedField === `user_${index}` ? 'Copied!' : 'Copy'}>
                            <IconButton
                              size="small"
                              onClick={() => handleCopyToClipboard(log.userIdHash, `user_${index}`)}
                            >
                              <CopyIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Metadata Hash:</strong>
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                          <code style={{ fontSize: '12px', wordBreak: 'break-all' }}>
                            {truncateHash(log.metaHash, 48)}
                          </code>
                          <Tooltip title={copied && copiedField === `meta_${index}` ? 'Copied!' : 'Copy'}>
                            <IconButton
                              size="small"
                              onClick={() => handleCopyToClipboard(log.metaHash, `meta_${index}`)}
                            >
                              <CopyIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                        <Button
                          size="small"
                          variant="outlined"
                          startIcon={<VerifiedUserIcon />}
                          fullWidth
                          onClick={() => {
                            setSelectedLog(log);
                            handleVerify(log.index);
                          }}
                          disabled={verifying}
                        >
                          Verify Integrity
                        </Button>
                      </CardContent>
                    </Card>
                  </TimelineContent>
                </TimelineItem>
              ))}
            </Timeline>
          )}

          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={(e, value) => setPage(value)}
            />
          </Box>
        </>
      )}

      <Dialog open={verificationDialog} onClose={() => setVerificationDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <VerifiedUserIcon />
          Integrity Verification Result
        </DialogTitle>
        <DialogContent>
          {verificationResult ? (
            <>
              {verificationResult.success ? (
                <>
                  {verificationResult.verified ? (
                    <Alert severity="success" sx={{ mb: 2 }}>
                      ✓ Metadata integrity verified successfully
                    </Alert>
                  ) : (
                    <Alert severity="warning" sx={{ mb: 2 }}>
                      ⚠ {verificationResult.reason || 'Verification inconclusive'}
                    </Alert>
                  )}
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                      Log Entry Details:
                    </Typography>
                    <Box sx={{ backgroundColor: '#f5f5f5', p: 2, borderRadius: 1, mb: 2 }}>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Event Type:</strong> {verificationResult.log_entry?.eventType}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Timestamp:</strong> {formatTimestamp(verificationResult.log_entry?.timestamp)}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>On-Chain Meta Hash:</strong>
                        <br />
                        <code style={{ fontSize: '11px', wordBreak: 'break-all' }}>
                          {verificationResult.log_entry?.metaHash}
                        </code>
                      </Typography>
                    </Box>
                    {verificationResult.stored_metadata && (
                      <>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                          Stored Metadata:
                        </Typography>
                        <Box sx={{ backgroundColor: '#f5f5f5', p: 2, borderRadius: 1 }}>
                          <pre style={{ fontSize: '11px', overflow: 'auto', maxHeight: '300px' }}>
                            {JSON.stringify(verificationResult.stored_metadata, null, 2)}
                          </pre>
                        </Box>
                      </>
                    )}
                  </Box>
                </>
              ) : (
                <Alert severity="error">
                  Error: {verificationResult.error}
                </Alert>
              )}
            </>
          ) : (
            <LinearProgress />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setVerificationDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
