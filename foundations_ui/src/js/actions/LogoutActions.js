import BaseActions from './BaseActions';

class LogoutActions {
  static getLogout(refreshToken) {
    const url = 'auth/logout';
    return BaseActions.getFromStagingAuthLogout(url, refreshToken);
  }
}
export default LogoutActions;
