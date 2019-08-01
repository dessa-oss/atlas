import React from 'react';
import { Redirect } from 'react-router-dom';


const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v1/',
  baseBetaURL: process.env.REACT_APP_BETA_API_URL || 'http://private-83924-dessa.apiary-mock.com/api/v2beta/',
  getFromAPI(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      credentials: 'include',
    })
      .then(
        (res) => {
          const { status } = res;
          const result = res.json();
          return Promise.all([status, result]);
        },
      ).catch(() => { return null; });
  },

  postToAPI(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'POST',
      body,
      credentials: 'include',
    }).then(
      (res) => {
        const { status } = res;
        const result = res.json();
        return Promise.all([status, result]);
      },
    ).catch(() => { return null; });
  },

  deleteBetaFromAPI(url, body) {
    const fullURL = this.baseBetaURL.concat(url);
    return fetch(fullURL, {
      method: 'DELETE',
      body,
      credentials: 'include',
    }).then(
      (res) => {
        const status = res.status;
        const result = res.json();
        return Promise.all([status, result]);
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
    return fetch(fullURL, {
      credentials: 'include',
    })
      .then(
        (res) => {
          const status = res.status;
          const result = res.json();
          return Promise.all([status, result]);
        },
      ).catch(
        (err) => {
          return null;
        },
      );
  },

  redirectRoute(urlName) {
    return <Redirect push to={urlName} />;
  },
};

export default BaseActions;
