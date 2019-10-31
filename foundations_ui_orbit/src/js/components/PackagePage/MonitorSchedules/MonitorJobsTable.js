import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";

class MonitorJobsTable extends Component {
  constructor(props) {
    super(props);
    const { location, monitorResult } = this.props;

    this.state = {
      rows: null,
      projectName: location.state.project.name,
      monitorName: monitorResult.properties.spec.environment.MONITOR_NAME
    };
    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  async reload() {
    const { projectName, monitorName } = this.state;
    const { onClickRow, reload, toggleLogsModal } = this.props;

    const result = await MonitorSchedulesActions.getMonitorJobs(projectName, monitorName);
    const rows = MonitorSchedulesActions.getMonitorJobRows(result, onClickRow, toggleLogsModal);
    this.setState({ rows: rows });
    reload();
  }

  render() {
    const { rows } = this.state;
    const { selectedRow } = this.props;

    let rowsWithProps = [];
    if (rows) {
      rowsWithProps = rows.map(row => React.cloneElement(
        row,
        { selectedRow: selectedRow }
      ));
    }

    return (
      <div className="monitor-jobs">
        <div className="monitor-jobs-heading">
          <h3>Monitor Jobs</h3>
          <div className="i--icon-delete" />
          <div className="i--icon-refresh" onClick={this.reload} />
        </div>
        <div className="monitor-job-listing">
          <div className="monitor-job-items">
            <div className="monitor-job-table-row" onClick={this.onClick}>
              <div className="monitor-job-checkbox" />
              <div className="monitor-job-name-cell">Job ID</div>
              <div className="monitor-job-status-cell">Status</div>
              <div className="monitor-job-launched-cell">Launched</div>
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
  onClickRow: PropTypes.func,
  selectedRow: PropTypes.object,
  reload: PropTypes.func,
  monitorResult: PropTypes.object,
  toggleLogsModal: PropTypes.func
};

MonitorJobsTable.defaultProps = {
  location: { state: {} },
  onClickRow: () => {},
  selectedRow: {},
  reload: () => {},
  monitorResult: {},
  toggleLogsModal: () => {}
};

export default MonitorJobsTable;
