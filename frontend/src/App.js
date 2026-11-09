import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import ProfileForm from './components/ProfileForm';
import Results from './components/Results';
import CareerBrowser from './components/CareerBrowser';
import CareerDetails from './components/CareerDetails';
import { Button, EmptyState } from './components/ui';

function NotFound() {
  return (
    <EmptyState
      title="Page not found"
      description="That route does not exist. The careers list is probably what you wanted."
      action={
        <Button as={Link} to="/careers" variant="primary">
          Browse careers
        </Button>
      }
    />
  );
}

export default function App() {
  return (
    <Router basename={process.env.PUBLIC_URL}>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<ProfileForm />} />
          <Route path="/results" element={<Results />} />
          <Route path="/careers" element={<CareerBrowser />} />
          <Route path="/careers/:id" element={<CareerDetails />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </Router>
  );
}
