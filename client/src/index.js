import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css"; // Global styles
import App from "./App"; // Main component
import reportWebVitals from "./reportWebVitals"; // Optional, for performance measuring

// Import Bootstrap CSS globally (already done in App.js, shown here for completeness)
import "bootstrap/dist/css/bootstrap.min.css";

// Create a root.
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the App component into the root.
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional: report web vitals
reportWebVitals();
