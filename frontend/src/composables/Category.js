import axios from "axios"


const Category = () => {

    const categoryName = async (category, token) => {

        try {

          const response = await axios.post("http://localhost:5000/admin/category",{ name:category }, { headers: {"Authorization" : `${token}`} });
          return response;
        } catch (err) {

          return err;
        }
    };


    const updateCategory = async (token, formData, id) => {

      try {

          let response = await axios.put('http://localhost:5000/admin/categories/'+id, {name:formData}, { headers: {"Authorization" : `${token}`} });
          return response;
      } catch (err) {

          return err.response;
      }
  };

    const categoryList = async (token) => {

      try {

        const response = await axios.get("http://localhost:5000/admin/category/list", { headers: {"Authorization" : `${token}`} });
        return response;
      } catch (err) {

        return err;
      }
  };


    return {
      
        categoryName,
        categoryList,
        updateCategory
    }
};

export default Category;