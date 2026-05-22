import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
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

  const registerUser = async (e) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.email.trim() || !formData.password.trim()) {
      alert("Please fill all required fields.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/register", formData);

      alert("Registration successful. Please login to continue.");
      navigate("/login");
    } catch (error) {
      console.error("Register error:", error.response?.data || error.message);
      alert(error.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="max-w-md mx-auto mt-16 bg-white p-8 rounded-xl shadow">
        <h2 className="text-3xl font-bold mb-6 text-indigo-600">
          Register
        </h2>

        <form onSubmit={registerUser} className="grid gap-4">
          <input
            className="border p-3 rounded"
            name="name"
            placeholder="Full Name"
            value={formData.name}
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
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="mt-4 text-sm text-gray-600">
          Already have an account?{" "}
          <Link to="/login" className="text-indigo-600 font-semibold">
            Login
          </Link>
        </p>
      </div>
    </>
  );
}

export default RegisterPage;