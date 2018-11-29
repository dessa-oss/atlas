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
      page: '',
      selectedProject: {},
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
      page, selectedProject, projects,
    } = this.state;

    let curPage = <ProjectPage selectProject={this.selectProject} projects={projects} />;

    if (page === 'jobList') {
      curPage = <JobListPage project={selectedProject} projectName={selectedProject.name} />;
    }

    return (
      <div className="App">
        {curPage}
      </div>
    );
  }
}

App.propTypes = {
  selectedProject: PropTypes.object,
  page: PropTypes.string,
};

App.defaultProps = {
  page: '',
  selectedProject: { name: 'local_deployment' },
};

export default App;
