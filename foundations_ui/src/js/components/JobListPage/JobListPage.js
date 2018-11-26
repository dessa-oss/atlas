import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTable from './JobTable';
import Toolbar from '../common/Toolbar';
import JobHeader from './JobHeader';

class JobListPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.projectName,
      project: this.props.project,
    };
  }

  render() {
    const { projectName, project } = this.state;
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader project={project} />
        <JobTable projectName={projectName} />
      </div>
    );
  }
}

JobListPage.propTypes = {
  projectName: PropTypes.string,
  project: PropTypes.object,
};

JobListPage.defaultProps = {
  projectName: '',
  project: {},
};

export default JobListPage;
