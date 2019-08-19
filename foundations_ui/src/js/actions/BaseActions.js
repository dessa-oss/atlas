const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL,
  baseApiaryURL: process.env.REACT_APP_APIARY_URL,

  get(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL)
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },

  getFromApiary(url) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL)
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },

  post(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },

  postApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },

  put(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },


  putApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'put',
      body: JSON.stringify(body),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },

  del(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: 'del',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },


  postJSONFile(url, fileName, data) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: 'post',
      body: JSON.stringify({ file: fileName, data }),
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(res => res.json())
      .then((result) => {
        return result;
      })
      .catch(() => {
        return null;
      });
  },
};

export default BaseActions;
