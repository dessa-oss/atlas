import { getFromStagingAuthLogout } from './BaseActions';

class LogoutActions {
  static getLogout() {
    const url = 'auth/logout';
    return getFromStagingAuthLogout(url);
  }
}
export default LogoutActions;
