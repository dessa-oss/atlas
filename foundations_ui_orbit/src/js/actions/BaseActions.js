import Cookies from 'js-cookie';
import CommonActions from './CommonActions';

const baseURL = process.env.REACT_APP_API_URL;
const baseApiaryURL = process.env.REACT_APP_APIARY_URL;
const baseMasterURL = process.env.REACT_APP_MASTER_URL;
const atlasURL = process.env.REACT_APP_ATLAS_URL;

const get = url => {
  const fullURL = baseURL.concat(url);
  const accessToken = CommonActions.getAccessCookie();
  return fetch(fullURL, {
    headers: {
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
      console.log('baseURL get error: ', error);
      return null;
    });
};

const getAtlas = url => {
  const fullURL = atlasURL.concat(url);
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
};

const delAtlas = url => {
  const fullURL = atlasURL.concat(url);
  const accessToken = CommonActions.getAccessCookie();
  return fetch(fullURL, {
    method: 'delete',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then(res => {
      CommonActions.checkStatusResponse(res);
      return res;
    })
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

const getMaster = url => {
  const fullURL = baseMasterURL.concat(url);
  return fetch(fullURL).then(res => {
    return res.json();
  });
};

const post = (url, body) => {
  const fullURL = baseURL.concat(url);
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
      return res;
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
  const accessToken = CommonActions.getAccessCookie();
  return fetch(fullURL, {
    method: 'PATCH',
    body: JSON.stringify(body),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then(res => {
      CommonActions.checkStatusResponse(res);
      return res;
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
    method: 'post',
    body: JSON.stringify(body),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
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
    method: 'post',
    body: JSON.stringify(body),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
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
      return res;
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
    method: 'put',
    body: JSON.stringify(body),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
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
  const accessToken = CommonActions.getAccessCookie();
  return fetch(fullURL, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  })
    .then(res => {
      CommonActions.checkStatusResponse(res);
      return res;
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
    method: 'post',
    body: JSON.stringify({ file: fileName, data: data }),
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })
    .then(res => res.json())
    .then(result => {
      return result;
    })
    .catch(() => {
      return null;
    });
};

const getFromStagingAuth = async (url, userpass) => {
  const fullURL = atlasURL.concat(url);
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
};

const getFromStagingAuthLogout = url => {
  const fullURL = atlasURL.concat(url);
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
};

export {
  get,
  getAtlas,
  delAtlas,
  getFromApiary,
  getMaster,
  post,
  postApiary,
  postMaster,
  put,
  putApiary,
  del,
  postJSONFile,
  patch,
  getFromStagingAuth,
  getFromStagingAuthLogout,
};
