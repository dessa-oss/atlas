import React, { Component } from "react";
import PropTypes from "prop-types";
import moment from "moment";

class MonitorJobTableRow extends Component {
  constructor(props) {
    super(props);
    const {
      status,
      launched,
      duration
    } = this.props;

    this.state = {
      status: status,
      launched: launched,
      duration: duration
    };

    this.onSelect = this.onSelect.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
    this.onOpenLogs = this.onOpenLogs.bind(this);
  }

  onSelect() {
    const { jobID, onSelect } = this.props;

    onSelect(jobID);
  }

  isSelectedRow() {
    const { jobID, selectedRows } = this.props;

    return selectedRows.has(jobID);
  }

  onOpenLogs() {
    const { onClickLogs, jobID } = this.props;
    onClickLogs(jobID);
  }

  render() {
    const {
      status,
      launched,
      duration
    } = this.state;
    const { jobID } = this.props;

    const selectedClass = this.isSelectedRow() ? "selected-row" : "";
    const formattedLaunchedTime = launched ? moment.unix(launched).format("YYYY-MM-DD HH:mm:ss") : "Not available";
    const launchTime = moment(launched);
    const endTime = moment(duration);
    const timeDiff = duration ? `${endTime.diff(launchTime)}s` : "Not available";

    function addStatus(rowStatus) {
      if (rowStatus === "completed") {
        return <div className="status-icon status-green" />;
      }

      if (rowStatus === "failed") {
        return <div className="status-icon status-red" />;
      }
      return <div className="status-icon status-running" />;
    }

    const statusIcon = addStatus(status);

    return (
      <div className={`monitor-job-table-row ${selectedClass}`}>
        <div className="monitor-job-checkbox"><input type="checkbox" onClick={this.onSelect} /></div>
        <div className="monitor-job-name-cell">{jobID}</div>
        <div className="monitor-job-status-cell">{statusIcon}</div>
        <div className="monitor-job-launched-cell">{formattedLaunchedTime}</div>
        <div className="monitor-job-duration-cell">{timeDiff}</div>
        <div className="monitor-job-open-cell">
          <div className="i--icon-open" onClick={this.onOpenLogs} />
        </div>
      </div>
    );
  }
}

MonitorJobTableRow.propTypes = {
  jobID: PropTypes.string,
  status: PropTypes.string,
  launched: PropTypes.number,
  duration: PropTypes.number,
  onSelect: PropTypes.func,
  selectedRows: PropTypes.object,
  onClickLogs: PropTypes.func
};

MonitorJobTableRow.defaultProps = {
  jobID: "Invalid job ID",
  status: "Missing",
  launched: "Missing",
  duration: "Missing",
  onSelect: () => {},
  selectedRows: new Set(),
  onClickLogs: () => {}
};


export default MonitorJobTableRow;
