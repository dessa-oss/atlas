import React from 'react';
import { Redirect } from 'react-router-dom';
import { getFromStagingAuth } from './BaseActions';

class LoginActions {
  static getLogin(username, password) {
    const encodedString = btoa(`${username}:${password}`);

    const url = 'auth/cli_login';
    return getFromStagingAuth(url, encodedString);
  }

  static redirect(urlName) {
    return <Redirect push to={urlName} />;
  }
}
export default LoginActions;
