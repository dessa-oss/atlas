import BaseActions from './BaseActions';

class LogoutActions {
  static getLogout() {
    const url = 'auth/logout';
    return BaseActions.getFromStagingAuthLogout(url);
  }
}
export default LogoutActions;
