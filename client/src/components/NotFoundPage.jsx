import React from 'react';
import { useNavigate } from 'react-router-dom';
import './NotFoundPage.css';

const NotFoundPage = () => {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className="not-found-container">
      <h1 className="not-found-title">404</h1>
      <h2 className="not-found-subtitle">Page Not Found</h2>
      <p className="not-found-text">
        Oops! The page you are looking for doesn't exist or has been moved.
      </p>
      <button className="go-back-button" onClick={handleGoBack}>
        Go to Homepage
      </button>
    </div>
  );
};

export default NotFoundPage;
