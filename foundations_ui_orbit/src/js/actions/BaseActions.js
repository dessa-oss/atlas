const baseURL = process.env.REACT_APP_API_URL;
const baseApiaryURL = process.env.REACT_APP_APIARY_URL;

const get = url => {
  const fullURL = baseURL.concat(url);
  return fetch(fullURL)
    .then(res => res.json())
    .then(result => {
      return result;
    })
    .catch(() => {
      return null;
    });
};

const getFromApiary = url => {
  const fullURL = baseApiaryURL.concat(url);
  return fetch(fullURL)
    .then(res => res.json())
    .then(result => {
      return result;
    })
    .catch(() => {
      return null;
    });
};

const post = (url, body) => {
  const fullURL = baseURL.concat(url);
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
    .catch(() => {
      return null;
    });
};

const postApiary = (url, body) => {
  const fullURL = baseApiaryURL.concat(url);
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
    .catch(() => {
      return null;
    });
};

const put = (url, body) => {
  const fullURL = baseURL.concat(url);
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
    .catch(() => {
      return null;
    });
};


const putApiary = (url, body) => {
  const fullURL = baseApiaryURL.concat(url);
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
    .catch(() => {
      return null;
    });
};

const del = url => {
  const fullURL = baseURL.concat(url);
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
    .catch(() => {
      return null;
    });
};


const postJSONFile = (url, fileName, data) => {
  const fullURL = baseApiaryURL.concat(url);
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
    .catch(() => {
      return null;
    });
};

export {
  get, getFromApiary, post, postApiary, put, putApiary, del, postJSONFile
};
