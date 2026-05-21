import { useEffect, useState } from "react";
import api from "../../services/api";
import Navbar from "../../components/Navbar";

function CustomerStories() {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    api.get("/blogs/public")
      .then((response) => setBlogs(response.data.blogs))
      .catch((error) => console.error(error));
  }, []);

  return (
    <>
      <Navbar />

      <div className="max-w-5xl mx-auto mt-10">
        <h2 className="text-3xl font-bold mb-6 text-indigo-600">
          Customer Stories
        </h2>

        <div className="grid md:grid-cols-2 gap-6">
          {blogs.map((blog) => (
            <div key={blog.blog_id} className="bg-white p-6 rounded-xl shadow">
              <h3 className="text-xl font-bold">{blog.title}</h3>
              <p className="text-gray-600 mt-2">By {blog.customer_name}</p>
              <p className="mt-2"><b>Rating:</b> {blog.rating}/5</p>
              <p><b>Category:</b> {blog.category}</p>
              <p><b>Sentiment:</b> {blog.sentiment}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default CustomerStories;