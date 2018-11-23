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
    };
  }

  render() {
    const { projectName } = this.state;
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader />
        <JobTable projectName={projectName} />
      </div>
    );
  }
}

JobListPage.propTypes = {
  projectName: PropTypes.string,
};

JobListPage.defaultProps = {
  projectName: '',
};

export default JobListPage;
