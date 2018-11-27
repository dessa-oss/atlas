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
    };
  }

  changePage(newPage) {
    this.setState({ page: newPage });
  }

  selectProject(project) {
    this.setState({ selectedProject: project, page: 'jobList' });
  }

  render() {
    const {
      page, selectedProject,
    } = this.state;

    let curPage = <ProjectPage selectProject={this.selectProject} />;

    if (page === 'jobList') {
      curPage = <JobListPage projectName={selectedProject} />;
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
