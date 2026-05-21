import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function MyTickets() {
  const [tickets, setTickets] = useState([]);
  const [email, setEmail] = useState(localStorage.getItem("userEmail") || "");
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

 const fetchTicketsByEmail = async (targetEmail) => {
  if (!targetEmail.trim()) {
    alert("Please enter your email to view tickets.");
    return;
  }

  try {
    setLoading(true);
    setSearched(true);

    const response = await api.get("/tickets/all");

    const filteredTickets = response.data.filter(
      (ticket) => ticket.email?.toLowerCase() === targetEmail.toLowerCase()
    );

    setTickets(filteredTickets);
  } catch (error) {
    console.error("Error fetching tickets:", error.response?.data || error.message);
    alert("Unable to fetch tickets. Please check backend.");
  } finally {
    setLoading(false);
  }
};

const fetchTickets = () => fetchTicketsByEmail(email); 

 
  const submitFeedback = async (ticketId, actualCsat) => {
    try {
      await api.put(`/tickets/${ticketId}/feedback`, {
        actual_csat: Number(actualCsat),
      });

      alert("CSAT feedback submitted successfully.");
      fetchTickets();
    } catch (error) {
      console.error("Feedback error:", error.response?.data || error.message);
      alert("Unable to submit feedback.");
    }
  };

  return (
    <>
      <Navbar />

      <div className="max-w-6xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6">
          My Tickets
        </h2>

        <div className="flex gap-4 mb-8">
          <input
            className="border p-3 rounded w-full"
            type="email"
            placeholder="Enter your email to view your tickets"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button
            onClick={fetchTickets}
            disabled={loading}
            className="bg-indigo-600 text-white px-6 rounded font-semibold hover:bg-indigo-700"
          >
            {loading ? "Loading..." : "Search"}
          </button>
        </div>

        {searched && tickets.length === 0 && (
          <p className="text-gray-600">No tickets found for this email.</p>
        )}

        {tickets.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="border p-3">ID</th>
                  <th className="border p-3">Product</th>
                  <th className="border p-3">Category</th>
                  <th className="border p-3">Priority</th>
                  <th className="border p-3">Sentiment</th>
                  <th className="border p-3">Predicted CSAT</th>
                  <th className="border p-3">Actual CSAT</th>
                  <th className="border p-3">Status</th>
                  <th className="border p-3">Feedback</th>
                </tr>
              </thead>

              <tbody>
                {tickets.map((ticket) => (
                  <tr key={ticket.ticket_id}>
                    <td className="border p-3">{ticket.ticket_id}</td>
                    <td className="border p-3">{ticket.product_name || "N/A"}</td>
                    <td className="border p-3">{ticket.category}</td>
                    <td className="border p-3">{ticket.priority}</td>
                    <td className="border p-3">{ticket.sentiment}</td>
                    <td className="border p-3">{ticket.predicted_csat}</td>
                    <td className="border p-3">{ticket.actual_csat || "Not given"}</td>
                    <td className="border p-3">
                      <span className="px-3 py-1 rounded-full bg-indigo-100 text-indigo-700">
                        {ticket.status}
                      </span>
                    </td>
                    <td className="border p-3">
                      <select
                        className="border p-2 rounded"
                        defaultValue=""
                        onChange={(e) => {
                          if (e.target.value) {
                            submitFeedback(ticket.ticket_id, e.target.value);
                          }
                        }}
                      >
                        <option value="">Rate</option>
                        <option value="1">1 - Very Bad</option>
                        <option value="2">2 - Bad</option>
                        <option value="3">3 - Neutral</option>
                        <option value="4">4 - Good</option>
                        <option value="5">5 - Excellent</option>
                      </select>
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

export default MyTickets;