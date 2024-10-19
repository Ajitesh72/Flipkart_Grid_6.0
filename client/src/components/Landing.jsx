import React from 'react';
import { Button, Typography, Box, Grid } from '@mui/material';

const Landing = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'background.default',
        padding: '20px',
      }}
    >
      <Typography variant="h2" color="text.primary" sx={{ mb: 4, textAlign: 'center' }}>
        Welcome to Inventory Scanner
      </Typography>
      
      <Typography variant="h6" color="text.secondary" sx={{ mb: 4, textAlign: 'center' }}>
        Streamline your inventory management with real-time scanning and analysis.
        Ensure every product is in perfect condition before it leaves the warehouse.
      </Typography>

      <Grid container spacing={4} justifyContent="center">
        {/* Image 1 */}
        <Grid item xs={12} sm={6} md={4}>
          <Box
            component="img"
            sx={{
              width: '100%',
              height: 'auto',
              borderRadius: '8px',
            }}
            alt="Scanning process"
            src="https://www.shutterstock.com/shutterstock/videos/3393977369/thumb/1.jpg?ip=x480"
          />
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'center', mt: 1 }}>
            Real-time product scanning and data capture
          </Typography>
        </Grid>

        {/* Image 2 */}
        <Grid item xs={12} sm={6} md={4}>
          <Box
            component="img"
            sx={{
              width: '100%',
              height: 'auto',
              borderRadius: '8px',
            }}
            alt="Analysis"
            src="data:image/jpeg;base64,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"
          />
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'center', mt: 1 }}>
            AI-powered analysis for quality control
          </Typography>
        </Grid>

        {/* Image 3 */}
        <Grid item xs={12} sm={6} md={4}>
          <Box
            component="img"
            sx={{
              width: '100%',
              height: 'auto',
              borderRadius: '8px',
            }}
            alt="Dashboard"
            src="https://miro.medium.com/v2/resize:fit:702/1*Ra02AqsQlC0KV229EvM98g.png"
          />
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'center', mt: 1 }}>
            Dashboard for real-time updates and insights
          </Typography>
        </Grid>
      </Grid>

      <Button variant="contained" color="primary" href="/signin" sx={{ mt: 6 }}>
        Sign In
      </Button>
    </Box>
  );
};

export default Landing;
