import React from 'react';
import { Redirect } from 'react-router-dom';
import BaseActions from './BaseActions';

class LoginActions {
  static getLogin(username, password) {
    const encodedString = btoa(`${username}:${password}`);

    const url = 'auth/cli_login';
    return BaseActions.getFromStagingAuth(url, encodedString);
  }

  static postLogin(body) {
    const url = 'login';
    return BaseActions.postToAPI(url, body);
  }

  static redirect(urlName) {
    return <Redirect push to={urlName} />;
  }
}
export default LoginActions;
