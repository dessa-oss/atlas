import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSyncPane } from 'react-scroll-sync';
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
      toggleDurationFilter: this.props.toggleDurationFilter,
      toggleJobIdFilter: this.props.toggleJobIdFilter,
      toggleStartTimeFilter: this.props.toggleStartTimeFilter,
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
      rowNumbers, jobRows, toggleUserFilter, toggleStatusFilter, toggleDurationFilter, toggleJobIdFilter,
      toggleStartTimeFilter,
    } = this.state;

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader />
        <div className="full-height">
          <div className="job-column-header-container">
            <JobColumnHeader title="Start Time" className="static-header" toggleFilter={toggleStartTimeFilter} />
            <JobColumnHeader
              title="Status"
              isStatus={isStatus}
              className="static-status-header"
              toggleFilter={toggleStatusFilter}
            />
            <JobColumnHeader title="Job ID" className="static-header" toggleFilter={toggleJobIdFilter} />
            <JobColumnHeader title="Duration" className="static-header" toggleFilter={toggleDurationFilter} />
            <JobColumnHeader title="User" className="static-header" toggleFilter={toggleUserFilter} />
          </div>
          <ScrollSyncPane group="vertical">
            <div className="table-row-number">
              {rowNumbers}
            </div>
          </ScrollSyncPane>
          <ScrollSyncPane group="vertical">
            <div className="job-table-row-container">
              {jobRows}
            </div>
          </ScrollSyncPane>
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
  toggleDurationFilter: PropTypes.func,
  toggleJobIdFilter: PropTypes.func,
  toggleStartTimeFilter: PropTypes.func,
};

TableStaticColumns.defaultProps = {
  rowNumbers: [],
  jobRows: [],
  toggleUserFilter: () => {},
  toggleStatusFilter: () => {},
  toggleDurationFilter: () => {},
  toggleJobIdFilter: () => {},
  toggleStartTimeFilter: () => {},
};

export default TableStaticColumns;
