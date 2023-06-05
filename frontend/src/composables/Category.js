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
        categoryList
    }
};

export default Category;