import BaseActions from './BaseActions';

class ProjectActions {
  static getProjects() {
    const url = 'projects';
    return BaseActions.getFromAPI(url)
      .then((res) => {
        return res;
      });
  }
}
export default ProjectActions;
