const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v1/',
  baseBetaURL: process.env.REACT_APP_BETA_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v2beta/',
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
  // NOTE this is the method for Beta backend only
  getBetaFromAPI(url) {
    const fullURL = this.baseBetaURL.concat(url);
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
