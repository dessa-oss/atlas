import Cookies from 'js-cookie';
import CommonActions from './CommonActions';

const BaseActions = {
  baseStagingURL: process.env.REACT_APP_API_STAGING_URL,

  getFromStaging: function (url) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(res => {
        CommonActions.checkStatusResponse(res);
        return res;
      })
      .then(res => {
        return res.json();
      })
      .catch(error => {
        console.log('getFromStaging error: ', error);
        return null;
      });
  },

  getFromStagingAuth: async function (url, userpass) {
    const fullURL = this.baseStagingURL.concat(url);
    try {
      const fetchResponse = await fetch(fullURL, { headers: { Authorization: `Basic ${userpass}` } });

      const userResponse = await fetchResponse.json();

      if (fetchResponse.status === 200) {
        Cookies.set('atlas_access_token', userResponse.access_token);
        Cookies.set('atlas_refresh_token', userResponse.refresh_token);
      }
      return fetchResponse;
    } catch (error) {
      return error;
    }
  },

  getFromStagingAuthLogout: function (url) {
    const fullURL = this.baseStagingURL.concat(url);
    const refreshToken = Cookies.get('atlas_refresh_token');
    return fetch(fullURL, {
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    })
      .then(result => {
        return result;
      })
      .catch(error => {
        console.log('getFromStagingAuthLogout error: ', error);
        return error;
      });
  },

  postStaging: function (url, body) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(res => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then(result => {
        return result;
      })
      .catch(error => {
        console.log(error);
        return null;
      });
  },

  putStaging: function (url, body) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(res => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then(result => {
        return result;
      })
      .catch(error => {
        console.log(error);
        return null;
      });
  },

  delStaging: function (url) {
    const fullURL = this.baseStagingURL.concat(url);
    const accessToken = CommonActions.getAccessCookie();
    return fetch(fullURL, {
      method: 'delete',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(res => {
        CommonActions.checkStatusResponse(res);
        return res.json();
      })
      .then(result => {
        return result;
      })
      .catch(error => {
        console.log(error);
        return null;
      });
  },
};

export default BaseActions;
