import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from '../common/TableSectionHeader';
import JobColumnHeader from '../common/JobColumnHeader';

const isStatus = true;

class TableStaticColumns extends Component {
  constructor(props) {
    super(props);
    this.state = {
      rowNumbers: this.props.rowNumbers,
      jobRows: this.props.jobRows,
      toggleUserFilter: this.props.toggleUserFilter,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        jobRows: nextProps.jobRows,
        rowNumbers: nextProps.rowNumbers,
      },
    );
  }

  render() {
    const { rowNumbers, jobRows, toggleUserFilter } = this.state;

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader />
        <div className="static-header-row-container">
          <div className="job-column-header-container">
            <JobColumnHeader title="Start Time" className="start-time-offset" />
            <JobColumnHeader
              title="Status"
              isStatus={isStatus}
              className="status-offset"
              toggleFilter={this.toggleStatusFilter}
            />
            <JobColumnHeader title="Job ID" className="job-id-offset" />
            <JobColumnHeader title="Duration" className="duration-offset" />
            <JobColumnHeader title="User" className="user-offset" toggleFilter={toggleUserFilter} />
          </div>
          <div className="table-row-number">
            {rowNumbers}
          </div>
          <div className="job-table-row-container">
            {jobRows}
          </div>
        </div>
      </div>
    );
  }
}

TableStaticColumns.propTypes = {
  rowNumbers: PropTypes.array,
  jobRows: PropTypes.array,
  toggleUserFilter: PropTypes.func,
};

TableStaticColumns.defaultProps = {
  rowNumbers: [],
  jobRows: [],
  toggleUserFilter: () => {},
};

export default TableStaticColumns;
