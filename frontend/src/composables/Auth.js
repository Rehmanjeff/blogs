import axios from "axios"

const Auth = () => {

    const login = async (email, password) => {
        try {
          const response = await axios.post(
            "http://localhost:5000/admin/login",
            { email, password });
          return response;
        } catch (err) {
          return err;
        }
      };


    return {
      
        login,
    
    }
};

export default Auth;