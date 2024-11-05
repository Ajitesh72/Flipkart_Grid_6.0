import React, { useState } from 'react';
import { Button, TextField, Box, Typography, Grid } from '@mui/material';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = () => {
    // Simple sign-in logic (for now just redirect)
    window.location.href = '/scan';
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
        <Box>
          <Typography variant="h4" color="text.primary" gutterBottom>
            Sign In
          </Typography>
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
          // backgroundColor: 'background.paper',
          backgroundColor: "#000",

        }}
      >
        <Box
          component="img"
          src="https://i.ytimg.com/vi/V69Fwk48MCE/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAQ7gxNyTA7pp_cwGIuNbipz3IbZA" // Replace with your image path
          alt="Sign In Image"
          sx={{
            maxWidth: '100%',
            maxHeight: '100%',
            objectFit: 'cover',
            background:"#111",
            backgroundColor:"#111"
          }}
        />
      </Grid>
    </Grid>
  );
};

export default SignIn;
