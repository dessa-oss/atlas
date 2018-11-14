import BaseActions from './BaseActions';

class ProjectActions {
  static getProjects() {
    const url = 'projects';
    return BaseActions.getFromAPI(url);
  }
}
export default ProjectActions;
