import React, { Component } from 'react';
import PropTypes from 'prop-types';
import MonitorSchedulesActions from '../../../actions/MonitorSchedulesActions';

class MonitorJobsTable extends Component {
  constructor(props) {
    super(props);
    const { location } = this.props;

    this.state = {
      rows: null,
      projectName: location.state.project.name,
      selectedRows: new Set(),
      isAscending: false,
    };

    this.onSelectRow = this.onSelectRow.bind(this);
    this.deleteJobs = this.deleteJobs.bind(this);
    this.reload = this.reload.bind(this);
    this.onClickSortByLaunched = this.onClickSortByLaunched.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    const { monitorResult } = this.props;

    const prevMonitorName = prevProps.monitorResult.properties.spec.environment.MONITOR_NAME;
    const curMonitorName = monitorResult.properties.spec.environment.MONITOR_NAME;

    if (prevMonitorName !== curMonitorName) {
      this.reload();
    }
  }

  async reload() {
    const { projectName, isAscending } = this.state;
    const { reload, toggleLogsModal, monitorResult } = this.props;

    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    console.log('Before getting', isAscending);
    const result = await MonitorSchedulesActions.getMonitorJobs(projectName, monitorName, isAscending);
    const rows = MonitorSchedulesActions.getMonitorJobRows(result, this.onSelectRow, toggleLogsModal);
    this.setState({ rows: rows });
    reload();
  }

  onSelectRow(jobID) {
    const { selectedRows } = this.state;

    if (selectedRows.has(jobID)) {
      selectedRows.delete(jobID);
    } else {
      selectedRows.add(jobID);
    }

    this.setState({ selectedRows: selectedRows });
  }

  async deleteJobs() {
    const { selectedRows, projectName } = this.state;
    const { monitorResult } = this.props;

    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    await MonitorSchedulesActions.deleteMonitorJobs(selectedRows, projectName, monitorName);
    this.setState({ selectedRows: new Set() });
    this.reload();
  }

  onClickSortByLaunched() {
    const { isAscending } = this.state;
    this.setState({ isAscending: !isAscending }, this.reload);
  }

  render() {
    const {
      rows,
      selectedRows,
      isAscending,
    } = this.state;

    let rowsWithProps = [];
    if (rows) {
      rowsWithProps = rows.map(row => React.cloneElement(
        row,
        { selectedRows: selectedRows },
      ));
    }

    const arrow = (
      <i
        onKeyPress={this.onClickSortByLaunched}
        tabIndex={0}
        role="button"
        onClick={this.onClickSortByLaunched}
        className={isAscending
          ? 'i--icon-arrow-up' : 'i--icon-arrow-down'}
      />
    );

    return (
      <div className="monitor-jobs">
        <div className="monitor-jobs-heading">
          <h3>Monitor Jobs</h3>
          <div className="i--icon-refresh" onClick={this.reload} />
          <div className="i--icon-delete" onClick={this.deleteJobs} />
        </div>
        <div className="monitor-job-listing">
          <div className="monitor-job-items">
            <div className="monitor-job-table-row" onClick={this.onClick}>
              <div className="monitor-job-checkbox" />
              <div className="monitor-job-name-cell">Job ID</div>
              <div className="monitor-job-status-cell">Status</div>
              <div className="monitor-job-launched-cell">
                Completed
                {arrow}
              </div>
              <div className="monitor-job-duration-cell">Duration</div>
            </div>
            {rowsWithProps}
          </div>
        </div>
      </div>
    );
  }
}

MonitorJobsTable.propTypes = {
  location: PropTypes.object,
  reload: PropTypes.func,
  monitorResult: PropTypes.object,
  toggleLogsModal: PropTypes.func,
};

MonitorJobsTable.defaultProps = {
  location: { state: {} },
  reload: () => {},
  monitorResult: {},
  toggleLogsModal: () => {},
};

export default MonitorJobsTable;