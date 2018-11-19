import React from 'react';
import BaseActions from './BaseActions';
import ProjectSummary from '../components/ProjectPage/ProjectSummary';

class ProjectActions {
  static getProjects() {
    const url = 'projects';
    return BaseActions.getFromAPI(url);
  }

  static getJobsForProject(projectName) {
    const url = 'projects/'.concat(projectName).concat('/job_listing');
    return BaseActions.getFromAPI(url);
  }

  static getAllProjects(projects, selectProject) {
    const projectList = [];
    projects.forEach((project) => {
      const key = project.name.concat('-').concat(project.created_at);
      projectList.push(<ProjectSummary
        key={key}
        project={project}
        selectProject={selectProject}
      />);
    });
    return projectList;
  }
}
export default ProjectActions;
