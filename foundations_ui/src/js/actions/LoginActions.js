import React from 'react';
import { Redirect } from 'react-router-dom';
import BaseActions from './BaseActions';

class LoginActions {
  static postLogin(body) {
    const url = 'login';
    return BaseActions.postFromAPI(url, body);
  }

  static redirect(urlName) {
    return <Redirect push to={urlName} />;
  }
}
export default LoginActions;
