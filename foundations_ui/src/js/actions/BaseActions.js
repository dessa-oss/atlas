const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v1/',
  baseJobURL: process.env.REACT_APP_API_JOB_URL || 'http://private-83924-dessa.apiary-mock.com/api/v2beta/',
  getFromAPI(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL)
      .then(
        res => res.json(),
      )
      .then(
        (result) => {
          return result;
        },
      ).catch(
        (err) => {
          return null;
        },
      );
  },
  // NOTE this is temp solely to work with API having Job list on a seperate route
  getJobsFromAPI(url) {
    const fullURL = this.baseJobURL.concat(url);
    return fetch(fullURL)
      .then(
        res => res.json(),
      )
      .then(
        (result) => {
          return result;
        },
      ).catch(
        (err) => {
          return null;
        },
      );
  },
};
export default BaseActions;
