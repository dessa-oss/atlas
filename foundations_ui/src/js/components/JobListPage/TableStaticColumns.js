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
      isStartTimeFiltered: this.props.isStartTimeFiltered,
      isStatusFiltered: this.props.isStatusFiltered,
      isJobIdFiltered: this.props.isJobIdFiltered,
      isDurationFiltered: this.props.isDurationFiltered,
      isUserFiltered: this.props.isUserFiltered,
      header: this.props.header,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        jobRows: nextProps.jobRows,
        rowNumbers: nextProps.rowNumbers,
        isStartTimeFiltered: nextProps.isStartTimeFiltered,
        isStatusFiltered: nextProps.isStatusFiltered,
        isJobIdFiltered: nextProps.isJobIdFiltered,
        isDurationFiltered: nextProps.isDurationFiltered,
        isUserFiltered: nextProps.isUserFiltered,
        header: nextProps.header,
      },
    );
  }

  render() {
    const {
      rowNumbers, jobRows, toggleUserFilter, toggleStatusFilter, toggleDurationFilter, toggleJobIdFilter,
      toggleStartTimeFilter, isStartTimeFiltered, isStatusFiltered, isJobIdFiltered, isDurationFiltered,
      isUserFiltered, header,
    } = this.state;

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader
          header={header}
        />
        <div className="full-height">
          <div className="job-column-header-container">
            <JobColumnHeader
              title="Job ID"
              className="static-header"
              toggleFilter={toggleJobIdFilter}
              isFiltered={isJobIdFiltered}
            />
            <JobColumnHeader
              title="Launched at"
              className="static-header"
              toggleFilter={toggleStartTimeFilter}
              isFiltered={isStartTimeFiltered}
            />
            <JobColumnHeader
              title="Status"
              isStatus={isStatus}
              className="static-status-header"
              toggleFilter={toggleStatusFilter}
              isFiltered={isStatusFiltered}
            />
            <JobColumnHeader
              title="Duration"
              className="static-header"
              toggleFilter={toggleDurationFilter}
              isFiltered={isDurationFiltered}
            />
            <JobColumnHeader
              title="User"
              className="static-header"
              toggleFilter={toggleUserFilter}
              isFiltered={isUserFiltered}
            />
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
  isStartTimeFiltered: PropTypes.bool,
  isStatusFiltered: PropTypes.bool,
  isJobIdFiltered: PropTypes.bool,
  isDurationFiltered: PropTypes.bool,
  isUserFiltered: PropTypes.bool,
  header: PropTypes.string,
};

TableStaticColumns.defaultProps = {
  rowNumbers: [],
  jobRows: [],
  toggleUserFilter: () => {},
  toggleStatusFilter: () => {},
  toggleDurationFilter: () => {},
  toggleJobIdFilter: () => {},
  toggleStartTimeFilter: () => {},
  isStartTimeFiltered: false,
  isStatusFiltered: false,
  isJobIdFiltered: false,
  isDurationFiltered: false,
  isUserFiltered: false,
  header: '',
};

export default TableStaticColumns;
