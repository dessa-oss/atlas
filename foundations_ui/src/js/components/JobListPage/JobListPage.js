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
      filters: [{ column: 'User', value: 'Buck' },
        { column: 'Status', value: 'Error' },
        { column: 'Start Time', value: 'Today' },
        { column: 'Metric 1', value: 'abc' },
        { column: 'Metric 2', value: '123' },
        { column: 'Metric 3', value: 'more words' },
      ],
    };
  }

  render() {
    const { projectName, project, filters } = this.state;
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader project={project} filters={filters} />
        <JobTable projectName={projectName} />
      </div>
    );
  }
}

JobListPage.propTypes = {
  projectName: PropTypes.string,
  project: PropTypes.object,
  filters: PropTypes.array,
};

JobListPage.defaultProps = {
  projectName: '',
  project: {},
  filters: [{ column: 'user', value: 'Buck' }],
};

export default JobListPage;
