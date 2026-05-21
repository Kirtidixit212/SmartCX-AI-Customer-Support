import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function AssignedTickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const agentName = localStorage.getItem("userName") || "Agent";

  const fetchAssignedTickets = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/tickets/agent/${agentName}/assigned`);
      setTickets(response.data);
    } catch (error) {
      console.error("Assigned tickets error:", error.response?.data || error.message);
      alert("Unable to fetch assigned tickets.");
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
      fetchAssignedTickets();
    } catch (error) {
      console.error("Status update error:", error.response?.data || error.message);
      alert("Unable to update ticket status.");
    }
  };

  const sendReply = async (ticketId) => {
    const replyBox = document.getElementById(`reply-${ticketId}`);
    const replyText = replyBox.value;

    if (!replyText.trim()) {
      alert("Reply cannot be empty.");
      return;
    }

    try {
      const response = await api.post(`/tickets/${ticketId}/reply`, {
        ticket_id: ticketId,
        agent_name: agentName,
        reply_text: replyText,
      });

      alert(
        `Reply sent successfully.\nReply Quality Score: ${response.data.reply_quality_score}/100`
      );

      fetchAssignedTickets();
    } catch (error) {
      console.error("Reply error:", error.response?.data || error.message);
      alert("Unable to send reply.");
    }
  };

  useEffect(() => {
    fetchAssignedTickets();
  }, []);

  return (
    <>
      <Navbar />

      <div className="max-w-7xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-3xl font-bold text-indigo-600">
              Assigned Tickets
            </h2>
            <p className="text-gray-600 mt-2">
              Agent: {agentName}
            </p>
          </div>

          <button
            onClick={fetchAssignedTickets}
            className="bg-indigo-600 text-white px-5 py-2 rounded font-semibold hover:bg-indigo-700"
          >
            Refresh
          </button>
        </div>

        {loading ? (
          <p>Loading assigned tickets...</p>
        ) : tickets.length === 0 ? (
          <div className="bg-gray-50 p-6 rounded-xl">
            <p className="text-gray-600">
              No tickets assigned to you yet. Admin must assign a ticket to:
              <b> {agentName}</b>
            </p>
          </div>
        ) : (
          <div className="grid gap-6">
            {tickets.map((ticket) => (
              <div key={ticket.ticket_id} className="border rounded-xl p-6 bg-gray-50">
                <div className="flex justify-between gap-4">
                  <div>
                    <h3 className="text-xl font-bold">
                      Ticket #{ticket.ticket_id} - {ticket.category}
                    </h3>
                    <p className="text-gray-600 mt-1">
                      Customer: {ticket.customer_name} | Product: {ticket.product_name || "N/A"}
                    </p>
                  </div>

                  <span className="px-3 py-1 rounded-full bg-orange-100 text-orange-700 h-fit">
                    {ticket.priority}
                  </span>
                </div>

                <p className="mt-4">
                  <b>Customer Message:</b> {ticket.message}
                </p>

                <div className="grid md:grid-cols-4 gap-4 mt-4 text-sm">
                  <p><b>Sentiment:</b> {ticket.sentiment}</p>
                  <p><b>Predicted CSAT:</b> {ticket.predicted_csat}</p>
                  <p><b>Risk Score:</b> {ticket.risk_score}%</p>
                  <p><b>Escalation:</b> {ticket.escalation_level}</p>
                </div>

                <div className="mt-4 bg-white p-4 rounded-lg border">
                  <b>Suggested Reply:</b>
                  <p className="mt-2 text-gray-700">{ticket.suggested_reply}</p>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mt-5">
                  <div>
                    <label className="block font-semibold mb-2">
                      Update Status
                    </label>

                    <select
                      className="border p-3 rounded w-full"
                      value={ticket.status}
                      onChange={(e) => updateStatus(ticket.ticket_id, e.target.value)}
                    >
                      <option value="Assigned">Assigned</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Escalated">Escalated</option>
                      <option value="Resolved">Resolved</option>
                      <option value="Closed">Closed</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-semibold mb-2">
                      Reply to Customer
                    </label>

                    <textarea
                      className="border p-3 rounded w-full"
                      rows="4"
                      defaultValue={ticket.suggested_reply}
                      id={`reply-${ticket.ticket_id}`}
                    />

                    <button
                      onClick={() => sendReply(ticket.ticket_id)}
                      className="bg-indigo-600 text-white px-5 py-2 rounded mt-2 hover:bg-indigo-700"
                    >
                      Send Reply
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

export default AssignedTickets;