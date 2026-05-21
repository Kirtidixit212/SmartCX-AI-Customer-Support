import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const userRole = localStorage.getItem("userRole");
  const userName = localStorage.getItem("userName");

  const logout = () => {
    localStorage.removeItem("userRole");
    localStorage.removeItem("userName");
    localStorage.removeItem("userEmail");
    navigate("/");
  };

  return (
    <nav className="bg-white shadow px-8 py-4 flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold text-indigo-600">
        SmartCX
      </Link>

      <div className="flex gap-6 text-sm font-medium items-center">
        <Link to="/" className="text-gray-700 hover:text-indigo-600">
          Home
        </Link>

        {!userRole && (
          <>
            <Link to="/stories" className="text-gray-700 hover:text-indigo-600">
              Customer Stories
            </Link>

            <Link to="/login" className="text-gray-700 hover:text-indigo-600">
              Login
            </Link>

            <Link to="/register" className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
              Register
            </Link>
          </>
        )}

        {userRole === "customer" && (
          <>
            <Link to="/submit-ticket" className="text-gray-700 hover:text-indigo-600">
              Submit Ticket
            </Link>

            <Link to="/my-tickets" className="text-gray-700 hover:text-indigo-600">
              My Tickets
            </Link>

            <Link to="/submit-blog" className="text-gray-700 hover:text-indigo-600">
              Submit Blog
            </Link>

            <Link to="/stories" className="text-gray-700 hover:text-indigo-600">
              Customer Stories
            </Link>
          </>
        )}

        {userRole === "admin" && (
          <>
            <Link to="/admin-dashboard" className="text-gray-700 hover:text-indigo-600">
              Admin Dashboard
            </Link>

            <Link to="/manage-tickets" className="text-gray-700 hover:text-indigo-600">
              Manage Tickets
            </Link>

            <Link to="/blog-approval" className="text-gray-700 hover:text-indigo-600">
              Blog Approval
            </Link>

            <Link to="/stories" className="text-gray-700 hover:text-indigo-600">
              Customer Stories
            </Link>
          </>
        )}

        {userRole === "agent" && (
          <>
            <Link to="/agent-dashboard" className="text-gray-700 hover:text-indigo-600">
              Agent Dashboard
            </Link>

            <Link to="/assigned-tickets" className="text-gray-700 hover:text-indigo-600">
              Assigned Tickets
            </Link>
          </>
        )}

        {userRole && (
          <>
            <span className="text-gray-500">
              {userName} ({userRole})
            </span>

            <button
              onClick={logout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;