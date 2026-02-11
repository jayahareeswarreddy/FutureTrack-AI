import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import ProfileForm from './components/ProfileForm';
import Results from './components/Results';
import CareerBrowser from './components/CareerBrowser';
import CareerDetails from './components/CareerDetails';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<ProfileForm />} />
          <Route path="/results" element={<Results />} />
          <Route path="/careers" element={<CareerBrowser />} />
          <Route path="/careers/:id" element={<CareerDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
