import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './components/Landing';
import SignIn from './components/SignIn';
import ScanAnalyze from './components/ScanAnalyze';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import NotFoundPage from './components/NotFoundPage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/scan" element={<ScanAnalyze />} />
          <Route path="/*" element={<NotFoundPage/>}/>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
