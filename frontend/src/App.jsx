import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/public/LandingPage";
import LoginPage from "./pages/public/LoginPage";
import CustomerStories from "./pages/public/CustomerStories";
import RegisterPage from "./pages/public/RegisterPage";
import SubmitTicket from "./pages/customer/SubmitTicket";
import MyTickets from "./pages/customer/MyTickets";
import SubmitBlog from "./pages/customer/SubmitBlog";

import AdminDashboard from "./pages/admin/AdminDashboard";
import ManageTickets from "./pages/admin/ManageTickets";
import BlogApproval from "./pages/admin/BlogApproval";
import AgentDashboard from "./pages/agent/AgentDashboard";
import AssignedTickets from "./pages/agent/AssignedTickets";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Pages */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/stories" element={<CustomerStories />} />

        {/* Customer Pages */}
        <Route path="/submit-ticket" element={<SubmitTicket />} />
        <Route path="/my-tickets" element={<MyTickets />} />
        <Route path="/submit-blog" element={<SubmitBlog />} />

        {/* Admin Pages */}
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
        <Route path="/manage-tickets" element={<ManageTickets />} />
        <Route path="/blog-approval" element={<BlogApproval />} />

        {/* Agent Pages */}
        <Route path="/agent-dashboard" element={<AgentDashboard />} />
        <Route path="/assigned-tickets" element={<AssignedTickets />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
