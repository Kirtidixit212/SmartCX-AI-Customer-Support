import { useState } from "react";
import api from "../../services/api";
import Navbar from "../../components/Navbar";

function SubmitTicket() {
  const [formData, setFormData] = useState({
    customer_name: localStorage.getItem("userName") || "",
    email: localStorage.getItem("userEmail") || "",
    order_id: "",
    product_name: "",
    message: "",
    channel: "Web",
    order_value: 0,
    previous_complaints: 0,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const submitTicket = async (e) => {
    e.preventDefault();

    const orderValue = Number(formData.order_value);
    const previousComplaints = Number(formData.previous_complaints);

    if (!formData.customer_name.trim()) {
      alert("Customer name is required.");
      return;
    }

    if (!formData.email.trim()) {
      alert("Email is required.");
      return;
    }

    if (!formData.message.trim()) {
      alert("Please describe your issue.");
      return;
    }

    if (isNaN(orderValue) || orderValue < 0) {
      alert("Order value must be a valid number.");
      return;
    }

    if (isNaN(previousComplaints) || previousComplaints < 0) {
      alert("Previous complaints must be a number. Use 0 if there are no previous complaints.");
      return;
    }

    const payload = {
      ...formData,
      order_value: orderValue,
      previous_complaints: previousComplaints,
    };

    try {
      setLoading(true);
      setResult(null);

      const response = await api.post("/tickets/create", payload);

      setResult(response.data);
    } catch (error) {
      console.error("Ticket submission error:", error.response?.data || error.message);

      if (error.response?.data?.detail) {
        alert(JSON.stringify(error.response.data.detail));
      } else {
        alert("Error submitting ticket. Please check that your backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="max-w-4xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <h2 className="text-3xl font-bold mb-6 text-indigo-600">
          Submit Support Ticket
        </h2>

        <form onSubmit={submitTicket} className="grid gap-4">
          <input
            className="border p-3 rounded"
            name="customer_name"
            placeholder="Customer Name"
            value={formData.customer_name}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="email"
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="order_id"
            placeholder="Order ID"
            value={formData.order_id}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="product_name"
            placeholder="Product Name"
            value={formData.product_name}
            onChange={handleChange}
          />

          <textarea
            className="border p-3 rounded"
            name="message"
            placeholder="Describe your issue"
            rows="5"
            value={formData.message}
            onChange={handleChange}
          />

          <select
            className="border p-3 rounded"
            name="channel"
            value={formData.channel}
            onChange={handleChange}
          >
            <option value="Web">Web</option>
            <option value="Email">Email</option>
            <option value="Chat">Chat</option>
            <option value="Call">Call</option>
          </select>

          <input
            className="border p-3 rounded"
            name="order_value"
            type="number"
            min="0"
            placeholder="Order Value"
            value={formData.order_value}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="previous_complaints"
            type="number"
            min="0"
            placeholder="Previous Complaints"
            value={formData.previous_complaints}
            onChange={handleChange}
          />

          <button
            type="submit"
            disabled={loading}
            className={`py-3 rounded-lg font-semibold text-white ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {loading ? "Submitting..." : "Submit Ticket"}
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-gray-100 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">AI Prediction Result</h3>

            <p><b>Category:</b> {result.category}</p>
            <p><b>Priority:</b> {result.priority}</p>
            <p><b>Sentiment:</b> {result.sentiment}</p>
            <p><b>Predicted CSAT:</b> {result.predicted_csat}</p>
            <p><b>Risk Score:</b> {result.risk_score}%</p>
            <p><b>Escalation:</b> {result.escalation_level}</p>
            <p><b>Status:</b> {result.status}</p>

            <div className="mt-4">
              <b>Suggested Reply:</b>
              <p className="mt-2">{result.suggested_reply}</p>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default SubmitTicket;