const baseURL = process.env.REACT_APP_API_URL;
const baseApiaryURL = process.env.REACT_APP_APIARY_URL;
const baseMasterURL = process.env.REACT_APP_MASTER_URL;
const atlasURL = process.env.REACT_APP_ATLAS_URL;

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

const getAtlas = url => {
  const fullURL = atlasURL.concat(url);
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

const getMaster = (url, body) => {
  const fullURL = baseMasterURL.concat(url);
  return fetch(fullURL).then(res => {
    return res.json();
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

const patch = (url, body) => {
  const fullURL = baseURL.concat(url);
  return fetch(fullURL, {
    method: "patch",
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

const postMaster = (url, body) => {
  const fullURL = baseMasterURL.concat(url);
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
  get, getAtlas, getFromApiary, getMaster, post, postApiary, postMaster, put, putApiary, del, postJSONFile, patch
};
