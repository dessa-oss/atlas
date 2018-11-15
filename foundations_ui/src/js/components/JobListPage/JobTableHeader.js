import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobColumnHeader from '../common/JobColumnHeader';
import TableSectionHeader from '../common/TableSectionHeader';
import InputMetric from '../common/InputMetric';

const isStatus = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
    };
  }

  render() {
    const { hiddenInputParams, allInputParams } = this.state;

    return (
      <div className="job-list-container">
        <TableSectionHeader />
        <InputMetric header="input parameter" hiddenInputParams={hiddenInputParams} allInputParams={allInputParams} />
        <InputMetric header="metrics" hiddenInputParams={hiddenInputParams} allInputParams={allInputParams} />
        <div className="job-column-header-container">
          <JobColumnHeader title="Start Time" className="start-time-offset" />
          <JobColumnHeader title="Status" isStatus={isStatus} className="status-offset" />
          <JobColumnHeader title="Job ID" className="job-id-offset" />
          <JobColumnHeader title="Duration" className="duration-offset" />
          <JobColumnHeader title="User" className="user-offset" />
        </div>
      </div>
    );
  }
}

JobTableHeader.propTypes = {
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
};

JobTableHeader.defaultProps = {
  hiddenInputParams: [],
  allInputParams: [],
};

export default JobTableHeader;
