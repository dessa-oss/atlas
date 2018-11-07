import React, { Component } from 'react';
import Toolbar from './Toolbar';
import ProjectActions from '../actions/ProjectActions';
import ProjectHeader from './ProjectHeader';
import ProjectSummary from './ProjectSummary';

class ProjectPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      projects: [],
    };
    this.getAllProjects = this.getAllProjects.bind(this);
  }

  componentDidMount() {
    this.getAllProjects();
  }

  async getAllProjects() {
    const apiProjects = await ProjectActions.getProjects();
    if (apiProjects != null) {
      this.setState({ projects: apiProjects, isLoaded: true });
    } else {
      this.setState({ projects: [], isLoaded: true });
    }
  }

  render() {
    const { isLoaded, projects } = this.state;
    let projectList;
    if (isLoaded) {
      if (projects.length === 0) {
        projectList = <p>No projects available</p>;
      } else {
        projectList = [];
        projects.forEach((project) => {
          const key = project.name.concat('-').concat(project.created_at);
          projectList.push(<ProjectSummary key={key} project={project} />);
        });
      }
    } else {
      projectList = <p>Loading projects</p>;
    }

    return (
      <div className="project-page-container">
        <Toolbar />
        <ProjectHeader />
        <div className="projects-body-container">
          {projectList}
        </div>
      </div>
    );
  }
}

export default ProjectPage;
