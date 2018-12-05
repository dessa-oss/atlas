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
      toggleStatusFilter: this.props.toggleStatusFilter,
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
    const {
      rowNumbers, jobRows, toggleUserFilter, toggleStatusFilter,
    } = this.state;

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader />
        <div className="full-height">
          <div className="job-column-header-container">
            <JobColumnHeader title="Start Time" className="static-header" />
            <JobColumnHeader
              title="Status"
              isStatus={isStatus}
              className="static-status-header"
              toggleFilter={toggleStatusFilter}
            />
            <JobColumnHeader title="Job ID" className="static-header" />
            <JobColumnHeader title="Duration" className="static-header" />
            <JobColumnHeader title="User" className="static-header" toggleFilter={toggleUserFilter} />
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
  toggleStatusFilter: PropTypes.func,
};

TableStaticColumns.defaultProps = {
  rowNumbers: [],
  jobRows: [],
  toggleUserFilter: () => {},
  toggleStatusFilter: () => {},
};

export default TableStaticColumns;
