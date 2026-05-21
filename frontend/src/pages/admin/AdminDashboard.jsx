import { useEffect, useState } from "react";
import api from "../../services/api";
import DashboardCard from "../../components/DashboardCard";
import Navbar from "../../components/Navbar";
import { Link } from "react-router-dom";

function AdminDashboard() {
  const [data, setData] = useState(null);
  const [categoryData, setCategoryData] = useState({});
  const [sentimentData, setSentimentData] = useState({});
  const [blogAnalytics, setBlogAnalytics] = useState(null);
  const [error, setError] = useState("");

  const fetchDashboard = async () => {
    try {
      setError("");

      const adminResponse = await api.get("/dashboard/admin");
      const categoryResponse = await api.get("/dashboard/ticket-category");
      const sentimentResponse = await api.get("/dashboard/sentiment");
      const blogResponse = await api.get("/dashboard/blog-analytics");

      setData(adminResponse.data);
      setCategoryData(categoryResponse.data || {});
      setSentimentData(sentimentResponse.data || {});
      setBlogAnalytics(blogResponse.data);
    } catch (error) {
      console.error("Dashboard error:", error.response?.data || error.message);
      setError("Unable to load admin dashboard. Please check backend server and dashboard APIs.");
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  return (
    <>
      <Navbar />

      <div className="p-10">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-indigo-600">
            Admin Dashboard
          </h2>

          <button
            onClick={fetchDashboard}
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
          <div className="bg-white p-6 rounded-xl shadow">
            <p>Loading dashboard...</p>
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-4 gap-6 mb-10">
              <DashboardCard title="Total Tickets" value={data.total_tickets} />
              <DashboardCard title="Pending Tickets" value={data.pending_tickets} />
              <DashboardCard title="Resolved Tickets" value={data.resolved_tickets} />
              <DashboardCard title="Average CSAT" value={data.average_csat} />
              <DashboardCard title="High Priority" value={data.high_priority_tickets} />
              <DashboardCard title="Negative Sentiment %" value={`${data.negative_sentiment_percent}%`} />
              <DashboardCard title="SLA Breaches" value={data.sla_breaches} />
              <DashboardCard title="Pending Blogs" value={data.pending_blog_approvals} />
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-10">
              <Link
                to="/manage-tickets"
                className="bg-white p-6 rounded-xl shadow hover:shadow-lg"
              >
                <h3 className="text-xl font-bold text-indigo-600">Manage Tickets</h3>
                <p className="text-gray-600 mt-2">View, assign, and update support tickets.</p>
              </Link>

              <Link
                to="/blog-approval"
                className="bg-white p-6 rounded-xl shadow hover:shadow-lg"
              >
                <h3 className="text-xl font-bold text-indigo-600">Blog Approval</h3>
                <p className="text-gray-600 mt-2">Approve or reject customer blogs.</p>
              </Link>

              <Link
                to="/stories"
                className="bg-white p-6 rounded-xl shadow hover:shadow-lg"
              >
                <h3 className="text-xl font-bold text-indigo-600">Public Stories</h3>
                <p className="text-gray-600 mt-2">View approved customer blogs.</p>
              </Link>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-xl font-bold mb-4">Ticket Categories</h3>

                {Object.keys(categoryData).length === 0 ? (
                  <p className="text-gray-600">No category data yet.</p>
                ) : (
                  Object.entries(categoryData).map(([category, count]) => (
                    <div key={category} className="flex justify-between border-b py-2">
                      <span>{category}</span>
                      <b>{count}</b>
                    </div>
                  ))
                )}
              </div>

              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-xl font-bold mb-4">Sentiment Distribution</h3>

                {Object.keys(sentimentData).length === 0 ? (
                  <p className="text-gray-600">No sentiment data yet.</p>
                ) : (
                  Object.entries(sentimentData).map(([sentiment, count]) => (
                    <div key={sentiment} className="flex justify-between border-b py-2">
                      <span>{sentiment}</span>
                      <b>{count}</b>
                    </div>
                  ))
                )}
              </div>

              <div className="bg-white p-6 rounded-xl shadow">
                <h3 className="text-xl font-bold mb-4">Blog Analytics</h3>

                {!blogAnalytics ? (
                  <p className="text-gray-600">No blog data yet.</p>
                ) : (
                  <>
                    <div className="flex justify-between border-b py-2">
                      <span>Total Blogs</span>
                      <b>{blogAnalytics.total_blogs}</b>
                    </div>

                    <div className="flex justify-between border-b py-2">
                      <span>Approved</span>
                      <b>{blogAnalytics.approved_blogs}</b>
                    </div>

                    <div className="flex justify-between border-b py-2">
                      <span>Pending</span>
                      <b>{blogAnalytics.pending_blogs}</b>
                    </div>

                    <div className="flex justify-between border-b py-2">
                      <span>Rejected</span>
                      <b>{blogAnalytics.rejected_blogs}</b>
                    </div>

                    <div className="flex justify-between border-b py-2">
                      <span>Average Rating</span>
                      <b>{blogAnalytics.average_rating}/5</b>
                    </div>
                  </>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default AdminDashboard;