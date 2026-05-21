import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import api from "../../services/api";

function BlogApproval() {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBlogs = async () => {
    try {
      setLoading(true);
      const response = await api.get("/blogs/all");
      setBlogs(response.data);
    } catch (error) {
      console.error("Error fetching blogs:", error.response?.data || error.message);
      alert("Unable to fetch blogs.");
    } finally {
      setLoading(false);
    }
  };

  const updateBlogStatus = async (blogId, status) => {
    try {
      await api.put(`/blogs/${blogId}/status`, {
        admin_status: status,
      });

      alert(`Blog ${status} successfully.`);
      fetchBlogs();
    } catch (error) {
      console.error("Blog status error:", error.response?.data || error.message);
      alert("Unable to update blog status.");
    }
  };

  useEffect(() => {
    fetchBlogs();
  }, []);

  return (
    <>
      <Navbar />

      <div className="max-w-7xl mx-auto mt-10 bg-white p-8 rounded-xl shadow">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-indigo-600">
            Admin - Blog Approval Panel
          </h2>

          <button
            onClick={fetchBlogs}
            className="bg-indigo-600 text-white px-5 py-2 rounded font-semibold hover:bg-indigo-700"
          >
            Refresh
          </button>
        </div>

        {loading ? (
          <p>Loading blogs...</p>
        ) : blogs.length === 0 ? (
          <p>No blogs found.</p>
        ) : (
          <div className="grid gap-6">
            {blogs.map((blog) => (
              <div key={blog.blog_id} className="border rounded-xl p-6 bg-gray-50">
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <h3 className="text-xl font-bold">{blog.title}</h3>
                    <p className="text-gray-600 mt-1">
                      By {blog.customer_name} | Rating: {blog.rating}/5
                    </p>
                  </div>

                  <span className="px-3 py-1 rounded-full bg-indigo-100 text-indigo-700">
                    {blog.admin_status}
                  </span>
                </div>

                <p className="mt-4 text-gray-800">
                  {blog.content}
                </p>

                <div className="grid md:grid-cols-3 gap-4 mt-4 text-sm">
                  <p><b>Category:</b> {blog.predicted_category}</p>
                  <p><b>Sentiment:</b> {blog.sentiment}</p>
                  <p><b>Moderation:</b> {blog.moderation_status}</p>
                </div>

                <div className="flex gap-3 mt-5">
                  <button
                    onClick={() => updateBlogStatus(blog.blog_id, "Approved")}
                    className="bg-green-600 text-white px-5 py-2 rounded hover:bg-green-700"
                  >
                    Approve
                  </button>

                  <button
                    onClick={() => updateBlogStatus(blog.blog_id, "Rejected")}
                    className="bg-red-600 text-white px-5 py-2 rounded hover:bg-red-700"
                  >
                    Reject
                  </button>

                  <button
                    onClick={() => updateBlogStatus(blog.blog_id, "Flagged")}
                    className="bg-yellow-500 text-white px-5 py-2 rounded hover:bg-yellow-600"
                  >
                    Flag
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

export default BlogApproval;