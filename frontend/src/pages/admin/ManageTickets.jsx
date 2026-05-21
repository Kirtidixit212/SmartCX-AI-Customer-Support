import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function ManageTickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      const response = await api.get("/tickets/all");
      setTickets(response.data);
    } catch (error) {
      console.error("Error fetching tickets:", error.response?.data || error.message);
      alert("Unable to fetch tickets.");
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (ticketId, status) => {
    try {
      await api.put(`/tickets/${ticketId}/status`, {
        status,
      });

      alert("Ticket status updated.");
      fetchTickets();
    } catch (error) {
      console.error("Status update error:", error.response?.data || error.message);
      alert("Unable to update status.");
    }
  };

  const assignAgent = async (ticketId, agentName) => {
    if (!agentName.trim()) {
      alert("Agent name cannot be empty.");
      return;
    }

    try {
      await api.put(`/tickets/${ticketId}/assign`, {
        assigned_agent: agentName,
      });

      alert("Ticket assigned successfully.");
      fetchTickets();
    } catch (error) {
      console.error("Assign error:", error.response?.data || error.message);
      alert("Unable to assign ticket.");
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  return (
    <>
      <Navbar />

      <div className="max-w-7xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-indigo-600">
            Admin - Manage Tickets
          </h2>

          <button
            onClick={fetchTickets}
            className="bg-indigo-600 text-white px-5 py-2 rounded font-semibold hover:bg-indigo-700"
          >
            Refresh
          </button>
        </div>

        {loading ? (
          <p>Loading tickets...</p>
        ) : tickets.length === 0 ? (
          <p>No tickets found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="border p-3">ID</th>
                  <th className="border p-3">Customer</th>
                  <th className="border p-3">Email</th>
                  <th className="border p-3">Message</th>
                  <th className="border p-3">Category</th>
                  <th className="border p-3">Priority</th>
                  <th className="border p-3">CSAT</th>
                  <th className="border p-3">Risk</th>
                  <th className="border p-3">Escalation</th>
                  <th className="border p-3">Agent</th>
                  <th className="border p-3">Status</th>
                  <th className="border p-3">Actions</th>
                </tr>
              </thead>

              <tbody>
                {tickets.map((ticket) => (
                  <tr key={ticket.ticket_id}>
                    <td className="border p-3">{ticket.ticket_id}</td>
                    <td className="border p-3">{ticket.customer_name}</td>
                    <td className="border p-3">{ticket.email}</td>
                    <td className="border p-3 max-w-xs">
                      {ticket.message?.slice(0, 80)}...
                    </td>
                    <td className="border p-3">{ticket.category}</td>
                    <td className="border p-3">
                      <span className="px-2 py-1 rounded bg-orange-100 text-orange-700">
                        {ticket.priority}
                      </span>
                    </td>
                    <td className="border p-3">{ticket.predicted_csat}</td>
                    <td className="border p-3">{ticket.risk_score}%</td>
                    <td className="border p-3">{ticket.escalation_level}</td>
                    <td className="border p-3">
                      {ticket.assigned_agent || "Not Assigned"}
                    </td>
                    <td className="border p-3">{ticket.status}</td>
                    <td className="border p-3">
                      <div className="flex flex-col gap-2">
                        <select
                          className="border p-2 rounded"
                          value={ticket.status}
                          onChange={(e) =>
                            updateStatus(ticket.ticket_id, e.target.value)
                          }
                        >
                          <option value="Pending">Pending</option>
                          <option value="Assigned">Assigned</option>
                          <option value="In Progress">In Progress</option>
                          <option value="Escalated">Escalated</option>
                          <option value="Resolved">Resolved</option>
                          <option value="Closed">Closed</option>
                        </select>

                        <input
                          className="border p-2 rounded"
                          placeholder="Agent name"
                          onKeyDown={(e) => {
                            if (e.key === "Enter") {
                              assignAgent(ticket.ticket_id, e.target.value);
                              e.target.value = "";
                            }
                          }}
                        />

                        <small className="text-gray-500">
                          Press Enter to assign
                        </small>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}

export default ManageTickets;