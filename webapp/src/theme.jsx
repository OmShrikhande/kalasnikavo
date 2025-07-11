import { createTheme } from '@mui/material/styles';
import { alpha } from '@mui/material/styles';

// Enhanced theme with modern design principles
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#6C63FF',
      light: '#8B85FF',
      dark: '#4B44CC',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FF6B6B',
      light: '#FF8A8A',
      dark: '#E55454',
      contrastText: '#ffffff',
    },
    background: {
      default: '#F8FAFC',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#1A202C',
      secondary: '#718096',
    },
    success: {
      main: '#48BB78',
      light: '#68D391',
      dark: '#38A169',
    },
    warning: {
      main: '#ED8936',
      light: '#F6AD55',
      dark: '#DD6B20',
    },
    error: {
      main: '#F56565',
      light: '#FC8181',
      dark: '#E53E3E',
    },
    info: {
      main: '#4299E1',
      light: '#63B3ED',
      dark: '#3182CE',
    },
    divider: alpha('#E2E8F0', 0.12),
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
      fontSize: '0.875rem',
    },
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.4,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.1em',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 1px 3px rgba(0, 0, 0, 0.05)',
    '0px 4px 6px rgba(0, 0, 0, 0.07)',
    '0px 5px 15px rgba(0, 0, 0, 0.08)',
    '0px 10px 24px rgba(0, 0, 0, 0.09)',
    '0px 15px 35px rgba(0, 0, 0, 0.1)',
    '0px 20px 40px rgba(0, 0, 0, 0.1)',
    '0px 25px 50px rgba(0, 0, 0, 0.12)',
    '0px 30px 60px rgba(0, 0, 0, 0.12)',
    '0px 35px 70px rgba(0, 0, 0, 0.13)',
    '0px 40px 80px rgba(0, 0, 0, 0.13)',
    '0px 45px 90px rgba(0, 0, 0, 0.14)',
    '0px 50px 100px rgba(0, 0, 0, 0.15)',
    '0px 55px 110px rgba(0, 0, 0, 0.15)',
    '0px 60px 120px rgba(0, 0, 0, 0.16)',
    '0px 65px 130px rgba(0, 0, 0, 0.16)',
    '0px 70px 140px rgba(0, 0, 0, 0.17)',
    '0px 75px 150px rgba(0, 0, 0, 0.17)',
    '0px 80px 160px rgba(0, 0, 0, 0.18)',
    '0px 85px 170px rgba(0, 0, 0, 0.18)',
    '0px 90px 180px rgba(0, 0, 0, 0.19)',
    '0px 95px 190px rgba(0, 0, 0, 0.19)',
    '0px 100px 200px rgba(0, 0, 0, 0.2)',
    '0px 105px 210px rgba(0, 0, 0, 0.2)',
    '0px 110px 220px rgba(0, 0, 0, 0.21)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.15)',
          },
        },
        contained: {
          boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0px 6px 20px rgba(0, 0, 0, 0.15)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          height: 6,
          backgroundColor: alpha('#E2E8F0', 0.3),
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
          color: '#1A202C',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRadius: '0 16px 16px 0',
          border: 'none',
          boxShadow: '0px 10px 40px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 16,
          boxShadow: '0px 20px 60px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiSnackbar: {
      styleOverrides: {
        root: {
          '& .MuiAlert-root': {
            borderRadius: 12,
          },
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&:hover': {
            backgroundColor: alpha('#6C63FF', 0.08),
          },
          '&.Mui-selected': {
            backgroundColor: alpha('#6C63FF', 0.12),
            '&:hover': {
              backgroundColor: alpha('#6C63FF', 0.16),
            },
          },
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          borderRadius: 8,
          margin: '0 4px',
          '&.Mui-selected': {
            backgroundColor: alpha('#6C63FF', 0.1),
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
        },
        head: {
          fontWeight: 600,
          backgroundColor: alpha('#F8FAFC', 0.8),
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          boxShadow: '0px 8px 24px rgba(0, 0, 0, 0.15)',
          '&:hover': {
            boxShadow: '0px 12px 32px rgba(0, 0, 0, 0.2)',
          },
        },
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          borderRadius: 8,
          backgroundColor: alpha('#1A202C', 0.9),
          fontSize: '0.75rem',
          fontWeight: 500,
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          '&:hover': {
            backgroundColor: alpha('#6C63FF', 0.08),
          },
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          '& .MuiSwitch-switchBase.Mui-checked': {
            color: '#6C63FF',
          },
          '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
            backgroundColor: '#6C63FF',
          },
        },
      },
    },
    MuiSlider: {
      styleOverrides: {
        root: {
          color: '#6C63FF',
          '& .MuiSlider-thumb': {
            boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.2)',
          },
        },
      },
    },
  },
});

// Dark theme variant
export const darkTheme = createTheme({
  ...theme,
  palette: {
    mode: 'dark',
    primary: {
      main: '#8B85FF',
      light: '#A8A3FF',
      dark: '#6C63FF',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#FF8A8A',
      light: '#FFA8A8',
      dark: '#FF6B6B',
      contrastText: '#ffffff',
    },
    background: {
      default: '#0F1419',
      paper: '#1A1F2E',
    },
    text: {
      primary: '#F7FAFC',
      secondary: '#A0AEC0',
    },
    divider: alpha('#E2E8F0', 0.12),
  },
  components: {
    ...theme.components,
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(26, 31, 46, 0.95)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
          color: '#F7FAFC',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
          backgroundColor: '#1A1F2E',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          backgroundColor: '#1A1F2E',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
        },
        head: {
          fontWeight: 600,
          backgroundColor: alpha('#0F1419', 0.8),
        },
      },
    },
  },
});

export default theme;