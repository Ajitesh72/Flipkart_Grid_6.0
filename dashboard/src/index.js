import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter,Router,Routes,Route } from "react-router-dom";
import NotFoundPage from "./components/NotFoundPage";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
    
      <App />
    </BrowserRouter>
  </React.StrictMode>

);
