import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function LoginPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    role: "customer",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const loginUser = async (e) => {
    e.preventDefault();

    if (!formData.email.trim() || !formData.password.trim()) {
      alert("Please enter email and password.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/login", formData);

      localStorage.setItem("userId", response.data.user_id);
      localStorage.setItem("userName", response.data.name);
      localStorage.setItem("userEmail", response.data.email);
      localStorage.setItem("userRole", response.data.role);

      alert("Login successful.");

      if (response.data.role === "admin") {
        navigate("/admin-dashboard");
      } else if (response.data.role === "agent") {
        navigate("/agent-dashboard");
      } else {
        navigate("/");
      }
    } catch (error) {
      console.error("Login error:", error.response?.data || error.message);
      alert(error.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="max-w-md mx-auto mt-16 bg-white p-8 rounded-xl shadow">
        <h2 className="text-3xl font-bold mb-6 text-indigo-600">
          Login
        </h2>

        <form onSubmit={loginUser} className="grid gap-4">
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
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
          />

          <select
            className="border p-3 rounded"
            name="role"
            value={formData.role}
            onChange={handleChange}
          >
            <option value="customer">Customer</option>
            <option value="agent">Support Agent</option>
            <option value="admin">Admin</option>
          </select>

          <button
            disabled={loading}
            className={`py-3 rounded-lg font-semibold text-white ${
              loading ? "bg-gray-400" : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="mt-4 text-sm text-gray-600">
          New user?{" "}
          <Link to="/register" className="text-indigo-600 font-semibold">
            Create account
          </Link>
        </p>
      </div>
    </>
  );
}

export default LoginPage;