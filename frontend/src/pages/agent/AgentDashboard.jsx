import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import DashboardCard from "../../components/DashboardCard";
import api from "../../services/api";
import { Link } from "react-router-dom";

function AgentDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const agentName = localStorage.getItem("userName") || "Agent";

  const fetchAgentDashboard = async () => {
    try {
      setError("");
      const response = await api.get(`/dashboard/agent/${agentName}`);
      setData(response.data);
    } catch (error) {
      console.error("Agent dashboard error:", error.response?.data || error.message);

      setError("Unable to load agent dashboard. Please check backend.");
      setData({
        agent_name: agentName,
        assigned_tickets: 0,
        high_priority_tickets: 0,
        resolved_tickets: 0,
        average_csat: 0,
      });
    }
  };

  useEffect(() => {
    fetchAgentDashboard();
  }, []);

  return (
    <>
      <Navbar />

      <div className="p-10 bg-gray-50 min-h-screen">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold text-indigo-600">
              Agent Dashboard
            </h2>
            <p className="text-gray-600 mt-2">
              Welcome, {agentName}. Manage your assigned customer support tickets.
            </p>
          </div>

          <button
            onClick={fetchAgentDashboard}
            className="bg-indigo-600 text-white px-5 py-2 rounded font-semibold hover:bg-indigo-700"
          >
            Refresh
          </button>
        </div>

        {error && (
          <div className="bg-red-100 text-red-700 p-4 rounded mb-6">
            {error}
          </div>
        )}

        {!data ? (
          <p>Loading agent dashboard...</p>
        ) : (
          <>
            <div className="grid md:grid-cols-4 gap-6 mb-10">
              <DashboardCard title="Assigned Tickets" value={data.assigned_tickets} />
              <DashboardCard title="High Priority" value={data.high_priority_tickets} />
              <DashboardCard title="Resolved Tickets" value={data.resolved_tickets} />
              <DashboardCard title="Average CSAT" value={data.average_csat} />
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <Link
                to="/assigned-tickets"
                className="bg-white p-6 rounded-xl shadow hover:shadow-lg"
              >
                <h3 className="text-xl font-bold text-indigo-600">
                  Assigned Tickets
                </h3>
                <p className="text-gray-600 mt-2">
                  View tickets assigned to you and reply to customers.
                </p>
              </Link>

              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-xl font-bold text-indigo-600">
                  AI Assistance
                </h3>
                <p className="text-gray-600 mt-2">
                  Use suggested replies, sentiment, priority, risk score, and CSAT prediction.
                </p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-xl font-bold text-indigo-600">
                  Workflow
                </h3>
                <p className="text-gray-600 mt-2">
                  Review ticket → send reply → update status → resolve issue.
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default AgentDashboard;