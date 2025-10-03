import React from 'react';
import { Link } from 'react-router-dom';

const NavBar: React.FC = () => (
  <nav className="bg-white shadow mb-6">
    <div className="container mx-auto px-4 py-3 flex justify-between items-center">
      <span className="font-bold text-xl">🌬️ HVAC AI Platform</span>
      <div className="space-x-4">
        <Link to="/" className="hover:underline">Dashboard</Link>
        <Link to="/simulation" className="hover:underline">Simulation</Link>
        <Link to="/monitoring" className="hover:underline">Monitoring</Link>
        <Link to="/prediction" className="hover:underline">Prediction</Link>
      </div>
    </div>
  </nav>
);

export default NavBar;
