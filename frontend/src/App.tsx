import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Communities from "./pages/Communities";
import CommunityDetail from "./pages/CommunityDetail";
import Dashboard from "./pages/Dashboard";
import ChartPage from "./pages/ChartPage";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Communities />} />
        <Route path="/community/:communityName" element={<CommunityDetail />} />
        <Route path="/community/:communityName/chart" element={<ChartPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
