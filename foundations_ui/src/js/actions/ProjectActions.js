import BaseActions from './BaseActions';

class ProjectActions {
  static getProjects() {
    const url = 'projects';
    return BaseActions.getFromAPI(url);
  }

  static getJobsForProject(projectName) {
    const url = 'projects/'.concat(projectName).concat('/job_listing');
    return BaseActions.getFromAPI(url);
  }
}
export default ProjectActions;
