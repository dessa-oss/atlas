const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v1/',
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
};
export default BaseActions;
