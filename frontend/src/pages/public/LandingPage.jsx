import Navbar from "../../components/Navbar";
import { Link } from "react-router-dom";

function LandingPage() {
  const userRole = localStorage.getItem("userRole");

  return (
    <>
      <Navbar />

      <section className="px-10 py-20 text-center bg-gradient-to-r from-indigo-600 to-blue-600 text-white">
        <h1 className="text-5xl font-bold mb-6">
          SmartCX: AI-Powered Customer Support Intelligence
        </h1>

        <p className="text-lg max-w-3xl mx-auto mb-8">
          Predict ticket category, priority, customer sentiment, CSAT score,
          risk level, and generate smart support replies using AI.
        </p>

        {!userRole ? (
          <div className="flex justify-center gap-4">
            <Link
              to="/login"
              className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
            >
              Login
            </Link>

            <Link
              to="/register"
              className="bg-yellow-400 text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-yellow-300"
            >
              Register
            </Link>

            <Link
              to="/stories"
              className="border border-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600"
            >
              View Customer Stories
            </Link>
          </div>
        ) : (
          <div className="flex justify-center gap-4">
            {userRole === "customer" && (
              <>
                <Link
                  to="/submit-ticket"
                  className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
                >
                  Submit Ticket
                </Link>

                <Link
                  to="/submit-blog"
                  className="bg-yellow-400 text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-yellow-300"
                >
                  Share Experience
                </Link>
              </>
            )}

            {userRole === "admin" && (
              <>
                <Link
                  to="/admin-dashboard"
                  className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
                >
                  Admin Dashboard
                </Link>

                <Link
                  to="/manage-tickets"
                  className="bg-yellow-400 text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-yellow-300"
                >
                  Manage Tickets
                </Link>
              </>
            )}

            {userRole === "agent" && (
              <Link
                to="/agent-dashboard"
                className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
              >
                Agent Dashboard
              </Link>
            )}

            <Link
              to="/stories"
              className="border border-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600"
            >
              View Customer Stories
            </Link>
          </div>
        )}
      </section>

      <section className="px-10 py-16 bg-gray-50">
        <h2 className="text-3xl font-bold text-center mb-10">
          Core Features
        </h2>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl shadow">
            <h3 className="font-bold text-xl mb-2">Ticket Intelligence</h3>
            <p>
              Automatically predict ticket category, priority, sentiment, CSAT,
              risk score, and escalation level.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <h3 className="font-bold text-xl mb-2">Agent Assistance</h3>
            <p>
              Generate suggested replies, check reply quality, and help agents
              resolve tickets faster.
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <h3 className="font-bold text-xl mb-2">Customer Voice</h3>
            <p>
              Customers can share experience blogs, which go through AI-based
              sentiment analysis and admin approval.
            </p>
          </div>
        </div>
      </section>

      <section className="px-10 py-16 bg-white">
        <h2 className="text-3xl font-bold text-center mb-10">
          How SmartCX Works
        </h2>

        <div className="grid md:grid-cols-4 gap-6 text-center">
          <div className="p-6 rounded-xl bg-gray-50 shadow">
            <h3 className="font-bold text-lg mb-2">1. Customer Submits Ticket</h3>
            <p className="text-gray-600">
              Customer enters issue details through the support form.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-gray-50 shadow">
            <h3 className="font-bold text-lg mb-2">2. AI Analyzes Issue</h3>
            <p className="text-gray-600">
              System predicts category, priority, sentiment, CSAT, and risk.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-gray-50 shadow">
            <h3 className="font-bold text-lg mb-2">3. Agent Takes Action</h3>
            <p className="text-gray-600">
              Agent uses suggested replies and resolves the ticket.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-gray-50 shadow">
            <h3 className="font-bold text-lg mb-2">4. Admin Tracks Insights</h3>
            <p className="text-gray-600">
              Admin monitors tickets, blogs, CSAT, risk, and performance.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}

export default LandingPage;