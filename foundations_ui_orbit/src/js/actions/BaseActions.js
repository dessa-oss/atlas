const BaseActions = {
  baseURL: process.env.REACT_APP_API_URL,
  baseApiaryURL: process.env.REACT_APP_APIARY_URL,
  get(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL)
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  getFromApiary(url) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL)
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  post(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: "post",
      body: JSON.stringify(body),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  postApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: "post",
      body: JSON.stringify(body),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  put(url, body) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: "put",
      body: JSON.stringify(body),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  putApiary(url, body) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: "put",
      body: JSON.stringify(body),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  delete(url) {
    const fullURL = this.baseURL.concat(url);
    return fetch(fullURL, {
      method: "del",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  },
  postJSONFile(url, fileName, data) {
    const fullURL = this.baseApiaryURL.concat(url);
    return fetch(fullURL, {
      method: "post",
      body: JSON.stringify({ file: fileName, data: data }),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(result => {
        return result;
      })
      .catch(err => {
        return null;
      });
  }
};
export default BaseActions;
