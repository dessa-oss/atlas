import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import ProjectActions from '../../actions/ProjectActions';
import Header from '../common/Header';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

class ProjectPage extends Component {
  constructor(props) {
    super(props);
    this.getAllProjects = this.getAllProjects.bind(this);
    this.setProjectList = this.setProjectList.bind(this);
    this.state = {
      isLoaded: false,
      projects: [],
      isMount: false,
      queryStatus: 200,
    };
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    this.getAllProjects();
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
  }

  async getAllProjects() {
    const [queryStatus, apiProjects] = await ProjectActions.getProjects();
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (apiProjects != null) {
        this.setState({ projects: apiProjects, isLoaded: true, queryStatus });
      } else {
        this.setState({ projects: [], isLoaded: true, queryStatus });
      }
    }
  }

  setProjectList() {
    const { projects, queryStatus } = this.state;
    if (queryStatus !== 200) {
      return <ErrorMessage errorCode={queryStatus} />;
    }
    if (projects.length === 0) {
      return <p>No projects available</p>;
    }
    return ProjectActions.getAllProjects(projects);
  }

  render() {
    const { isLoaded, projects, queryStatus } = this.state;
    let projectList;
    if (isLoaded) {
      if (queryStatus === 401) {
        return ProjectActions.redirect('/login');
      }
      projectList = this.setProjectList();
    } else {
      projectList = <Loading loadingMessage="We are currently loading your projects" />;
    }

    return (
      <div className="project-page-container">
        <div className="header">
          <Toolbar />
          <Header pageTitle="Projects" numProjects={projects.length} />
        </div>
        <div className="projects-body-container">
          {projectList}
        </div>
      </div>
    );
  }
}

ProjectPage.propTypes = {
  isMount: PropTypes.bool,
  isLoaded: PropTypes.bool,
  queryStatus: PropTypes.number,
  projects: PropTypes.array,
};

ProjectPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  queryStatus: 200,
  projects: [],
};

export default ProjectPage;
