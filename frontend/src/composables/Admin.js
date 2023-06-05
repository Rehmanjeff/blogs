import axios from "axios"


const Admin = () => {

    const dashboard = async (token) => {

        try {

            let response = await axios.get('http://localhost:5000/admin/dashboard', { headers: {"Authorization" : `${token}`} });
            return response;
        } catch (err) {

            return err.response;
        }
    };

    return {
      
        dashboard
    }
};

export default Admin;