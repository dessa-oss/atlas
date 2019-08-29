import React from 'react';
import BaseActions from './BaseActions';
import ProjectSummary from '../components/ProjectPage/ProjectSummary';

class ProjectActions {
  static getProjects() {
    const url = 'projects';
    return BaseActions.getFromAPI(url);
  }

  static getAllProjects(projects) {
    const projectList = [];
    projects.forEach((project) => {
      const key = project.name.concat('-').concat(project.created_at);
      projectList.push(<ProjectSummary
        key={key}
        project={project}
      />);
    });
    return projectList;
  }
}
export default ProjectActions;
