import axios from "axios"


const Author = () => {

    const createAuthor = async (token, formData) => {

        try {

            let response = await axios.post('http://localhost:5000/admin/authors', {name:formData}, { headers: {"Authorization" : `${token}`} });
            return response;
        } catch (err) {

            return err.response;
        }
    };

    const updateAuthor = async (token, formData, id) => {

        try {

            let response = await axios.put('http://localhost:5000/admin/authors/'+id, formData, { headers: {"Authorization" : `${token}`} });
            return response;
        } catch (err) {

            return err.response;
        }
    };

    const listAuthors = async (token) => {

        try {

            let response = await axios.get('http://localhost:5000/admin/authors', { headers: {"Authorization" : `${token}`} });
            return response;
        } catch (err) {

            return err.response;
        }
    };

    return {
      
        createAuthor,
        listAuthors,
        updateAuthor
    }
};

export default Author;