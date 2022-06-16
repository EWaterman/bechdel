import axios from 'axios';

// GET requests. Results are outup as a promise object
// TODO: add query param support
export const getRestCall = async (uri) => {
  return axios
    .get(uri)
    .then(({ data }) => data.results)
    .catch((err) => console.log(err));

  //   try {
  //     const response = await axios.get(uri);
  //     return response.data.results;
  //   } catch (errors) {
  //     console.error(errors);
  //   }
};
