import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import ChartPage from "./pages/ChartPage";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function ChartPageWrapper() {
  const query = useQuery();
  const company = query.get('company') || 'All';
  return <ChartPage selectedCompany={company} />;
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chart" element={<ChartPageWrapper />} />
      </Routes>
    </Router>
  );
}

export default App;
