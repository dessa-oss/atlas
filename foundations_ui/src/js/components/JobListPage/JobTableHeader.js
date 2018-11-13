import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobColumnHeader from '../common/JobColumnHeader';
import TableSectionHeader from '../common/TableSectionHeader';
import InputMetric from '../common/InputMetric';

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hiddenInputParams: this.props.hiddenInputParams,
    };
  }

  render() {
    const { hiddenInputParams } = this.state;
    return (
      <div className="job-list-container">
        <TableSectionHeader />
        <InputMetric header="input parameter" hiddenInputParams={hiddenInputParams} />
        <InputMetric header="metrics" />
        <JobColumnHeader title="Start Time" className="start-time-offset" />
        <JobColumnHeader title="Status" isStatus={1} className="status-offset" />
        <JobColumnHeader title="Job ID" className="job-id-offset" />
        <JobColumnHeader title="Duration" className="duration-offset" />
        <JobColumnHeader title="User" className="user-offset" />
      </div>
    );
  }
}

JobTableHeader.propTypes = {
  hiddenInputParams: PropTypes.array,
};

JobTableHeader.defaultProps = {
  hiddenInputParams: [],
};

export default JobTableHeader;
