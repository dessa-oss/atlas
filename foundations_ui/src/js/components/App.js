import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ProjectPage from './ProjectPage/ProjectPage';
import JobListPage from './JobListPage/JobListPage';
import ProjectActions from '../actions/ProjectActions';

class App extends Component {
  constructor(props) {
    super(props);
    this.changePage = this.changePage.bind(this);
    this.selectProject = this.selectProject.bind(this);
    this.state = {
      page: '',
      selectedProject: 'local_deployment',
      jobs: [],
    };
  }

  changePage(newPage) {
    this.setState({ page: newPage });
  }

  selectProject(project) {
    const projectJobs = ProjectActions.getJobsForProject(project);
    this.setState({ selectedProject: project, jobs: projectJobs, page: 'jobList' });
  }

  render() {
    const {
      page, selectedProject, jobs,
    } = this.state;

    let curPage = <ProjectPage selectProject={this.selectProject} />;

    if (page === 'jobList') {
      curPage = <JobListPage projectName={selectedProject} jobs={jobs} />;
    }

    return (
      <div className="App">
        {curPage}
      </div>
    );
  }
}

App.propTypes = {
  selectedProject: PropTypes.string,
  page: PropTypes.string,
  jobs: PropTypes.array,
};

App.defaultProps = {
  page: '',
  selectedProject: '',
  jobs: [],
};

export default App;
