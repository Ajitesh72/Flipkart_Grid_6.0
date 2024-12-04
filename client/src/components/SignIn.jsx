import React, { useState } from 'react';
import { Button, TextField, Box, Typography, Grid, Alert } from '@mui/material';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSignIn = () => {
    // Check for valid credentials
    if (email === 'athsankhe@gmail.com' && password === 'ath123') {
      // Store signed-in status in localStorage
      localStorage.setItem('signedIn', 'true');
      localStorage.setItem('user', 'athsankhe');
      // Redirect to /scan
      window.location.href = '/scan';
    } else {
      // Show error message
      setError(true);
    }
  };

  return (
    <Grid
      container
      sx={{
        minHeight: '100vh',
        backgroundColor: 'background.default',
      }}
    >
      {/* Left side - Sign in form */}
      <Grid
        item
        xs={12}
        md={6}
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: 3,
        }}
      >
        <Box sx={{ width: '100%', maxWidth: 400 }}>
          <Typography variant="h4" color="text.primary" gutterBottom>
            Sign In
          </Typography>
          {error && (
            <Alert severity="error" onClose={() => setError(false)}>
              Please use proper credentials.
            </Alert>
          )}
          <TextField
            label="Email"
            variant="outlined"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            sx={{ marginBottom: '16px', width: '100%' }}
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ marginBottom: '16px', width: '100%' }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSignIn}
            sx={{ width: '100%' }}
          >
            Sign In
          </Button>
        </Box>
      </Grid>

      {/* Right side - Image */}
      <Grid
        item
        xs={12}
        md={6}
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: '#000',
        }}
      >
        <Box
          component="img"
          src="https://i.ytimg.com/vi/V69Fwk48MCE/hq720.jpg"
          alt="Sign In Image"
          sx={{
            maxWidth: '100%',
            maxHeight: '100%',
            objectFit: 'cover',
          }}
        />
      </Grid>
    </Grid>
  );
};

export default SignIn;
