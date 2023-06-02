import axios from "axios"


const Auth = () => {

    const login = async (email, password) => {

        try {

          const response = await axios.post("http://localhost:5000/admin/login",{ email, password });
          return response;
        } catch (err) {

          return err;
        }
    };

    const logout = async (token) => {

        try {

            let response = await axios.post('http://localhost:5000/admin/logout',{}, { headers: {"Authorization" : `Bearer ${token}`} });
            if(response.status == 200){

                localStorage.removeItem('blogsAccessToken')
                localStorage.removeItem('blogsRefreshToken')
                localStorage.removeItem('userId')

            }

            return response;
        } catch (err) {

            return err.response;
        }
    };

    return {
      
        login,
        logout
    }
};

export default Auth;