import React from 'react';
import { Redirect } from 'react-router-dom';
import BaseActions from './BaseActions';

class LoginActions {
  static postLogin() {
    const url = 'login';
    return BaseActions.postFromAPI(url);
  }

  static redirect(urlName) {
    return <Redirect push to={urlName} />;
  }
}
export default LoginActions;
