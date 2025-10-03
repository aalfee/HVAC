import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Dashboard from './pages/Dashboard';
import Simulation from './pages/Simulation';
import Monitoring from './pages/Monitoring';
import Prediction from './pages/Prediction';

const AppRouter: React.FC = () => (
  <Router>
    <NavBar />
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/simulation" element={<Simulation />} />
      <Route path="/monitoring" element={<Monitoring />} />
      <Route path="/prediction" element={<Prediction />} />
    </Routes>
  </Router>
);

export default AppRouter;
