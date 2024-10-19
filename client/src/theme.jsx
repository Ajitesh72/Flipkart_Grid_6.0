import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1a237e', // Change to the dark blue used in your dashboard
    },
    secondary: {
      main: '#ff9800',
    },
    background: {
      default: '#1c1e29', // Dark theme background
      paper: '#2c2f36',
    },
    text: {
      primary: '#e0e0e0',
      secondary: '#4cceac',
    },
  },
});

export default theme;
