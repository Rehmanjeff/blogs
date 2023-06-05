import axios from "axios"


const Blog = () => {

    const createBlog = async (token, formData) => {

        try {

          const response = await axios.post("http://localhost:5000/admin/blogs", formData, { headers: {"Authorization" : `${token}`} });
          return response;
        } catch (err) {

          return err;
        }
    };

    const listBlogs = async (token, formData) => {

        try {

          const response = await axios.get("http://localhost:5000/admin/blogs", { headers: {"Authorization" : `${token}`} });
          return response;
        } catch (err) {

          return err;
        }
    };

    const readBlog = async (token, id) => {

        try {

          const response = await axios.get("http://localhost:5000/admin/blogs/" + id, { headers: {"Authorization" : `${token}`} });
          return response;
        } catch (err) {

          return err;
        }
    };

    const updateBlog = async (token, formData, id) => {

        try {

            let response = await axios.put('http://localhost:5000/admin/blogs/'+id, formData, { headers: {"Authorization" : `${token}`} });
            return response;
        } catch (err) {

            return err.response;
        }
    };


    return {
      
        createBlog,
        listBlogs,
        readBlog,
        updateBlog
    }
};

export default Blog;