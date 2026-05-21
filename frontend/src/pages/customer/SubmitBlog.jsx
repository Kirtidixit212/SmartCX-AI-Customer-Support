import { useState } from "react";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function SubmitBlog() {
  const [formData, setFormData] = useState({
    customer_name: "",
    title: "",
    content: "",
    rating: 5,
    order_id: "",
    product_name: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const submitBlog = async (e) => {
    e.preventDefault();

    if (!formData.customer_name.trim()) {
      alert("Customer name is required.");
      return;
    }

    if (!formData.title.trim()) {
      alert("Blog title is required.");
      return;
    }

    if (!formData.content.trim()) {
      alert("Blog content is required.");
      return;
    }

    if (formData.content.trim().split(" ").length < 10) {
      alert("Blog content should contain at least 10 words.");
      return;
    }

    try {
      setLoading(true);
      setResult(null);

      const response = await api.post("/blogs/create", {
        ...formData,
        rating: Number(formData.rating),
      });

      setResult(response.data);
    } catch (error) {
      console.error("Blog submission error:", error.response?.data || error.message);
      alert("Unable to submit blog.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="max-w-4xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6">
          Share Your Customer Experience
        </h2>

        <form onSubmit={submitBlog} className="grid gap-4">
          <input
            className="border p-3 rounded"
            name="customer_name"
            placeholder="Customer Name"
            value={formData.customer_name}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="order_id"
            placeholder="Order ID optional"
            value={formData.order_id}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="product_name"
            placeholder="Product Name optional"
            value={formData.product_name}
            onChange={handleChange}
          />

          <input
            className="border p-3 rounded"
            name="title"
            placeholder="Blog Title"
            value={formData.title}
            onChange={handleChange}
          />

          <textarea
            className="border p-3 rounded"
            name="content"
            placeholder="Write your experience..."
            rows="7"
            value={formData.content}
            onChange={handleChange}
          />

          <select
            className="border p-3 rounded"
            name="rating"
            value={formData.rating}
            onChange={handleChange}
          >
            <option value="5">5 - Excellent</option>
            <option value="4">4 - Good</option>
            <option value="3">3 - Neutral</option>
            <option value="2">2 - Bad</option>
            <option value="1">1 - Very Bad</option>
          </select>

          <button
            type="submit"
            disabled={loading}
            className={`py-3 rounded-lg font-semibold text-white ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {loading ? "Submitting..." : "Submit Blog"}
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-gray-100 p-6 rounded-xl">
            <h3 className="text-2xl font-bold mb-4">Blog Analysis Result</h3>

            <p><b>Blog ID:</b> {result.blog_id}</p>
            <p><b>Title:</b> {result.title}</p>
            <p><b>Rating:</b> {result.rating}/5</p>
            <p><b>Predicted Category:</b> {result.predicted_category}</p>
            <p><b>Sentiment:</b> {result.sentiment}</p>
            <p><b>Moderation:</b> {result.moderation_status}</p>
            <p><b>Admin Status:</b> {result.admin_status}</p>

            <p className="mt-4 text-gray-700">
              Your blog has been submitted for admin approval. Once approved,
              it will appear on the Customer Stories page.
            </p>
          </div>
        )}
      </div>
    </>
  );
}

export default SubmitBlog;