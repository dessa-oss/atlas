import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ProjectPage from './ProjectPage/ProjectPage';
import JobListPage from './JobListPage/JobListPage';

class App extends Component {
  constructor(props) {
    super(props);
    this.changePage = this.changePage.bind(this);
    this.selectProject = this.selectProject.bind(this);
    this.state = {
      page: 'jobList',
      selectedProject: 'local_deployment',
    };
  }

  changePage(newPage) {
    this.setState({ page: newPage });
  }

  selectProject(project) {
    this.setState({ selectedProject: project });
  }

  render() {
    const { page, selectedProject } = this.state;

    let curPage = <ProjectPage />;

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
};

App.defaultProps = {
  page: '',
  selectedProject: '',
};

export default App;
