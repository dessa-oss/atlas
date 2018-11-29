import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTable from './JobTable';
import Toolbar from '../common/Toolbar';
import JobHeader from './JobHeader';
import CommonActions from '../../actions/CommonActions';

class JobListPage extends Component {
  constructor(props) {
    super(props);
    this.updateHiddenStatus = this.updateHiddenStatus.bind(this);
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
      statuses: [
        { name: 'Completed', hidden: false },
        { name: 'Processing', hidden: false },
        { name: 'Error', hidden: false },
      ],
    };
  }

  updateHiddenStatus(hiddenFields) {
    const { statuses } = this.state;
    const statusNamesArray = statuses.map(status => status.name);
    const formattedColumns = CommonActions.formatColumns(statusNamesArray, hiddenFields);
    this.setState({ statuses: formattedColumns });
    this.forceUpdate();
  }

  render() {
    const {
      projectName, project, filters, statuses,
    } = this.state;
    return (
      <div>
        <Toolbar />
        <JobHeader project={project} filters={filters} />
        <JobTable projectName={projectName} statuses={statuses} updateHiddenStatus={this.updateHiddenStatus} />
      </div>
    );
  }
}

JobListPage.propTypes = {
  projectName: PropTypes.string,
  project: PropTypes.object,
  filters: PropTypes.array,
  statuses: PropTypes.array,
};

JobListPage.defaultProps = {
  projectName: '',
  project: {},
  filters: [],
  statuses: [],
};

export default JobListPage;
