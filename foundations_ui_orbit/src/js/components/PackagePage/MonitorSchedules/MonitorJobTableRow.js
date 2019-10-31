import React, { Component } from "react";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";
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

    this.onClick = this.onClick.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
    this.onOpenLogs = this.onOpenLogs.bind(this);
  }

  onClick() {
    const {
      status,
      launched,
      duration
    } = this.state;
    const { jobID, onClick } = this.props;

    onClick({
      jobID: jobID,
      status: status,
      launched: launched,
      duration: duration
    });
  }

  isSelectedRow() {
    const {
      status,
      launched,
      duration
    } = this.state;
    const { jobID, selectedRow } = this.props;
    const thisRow = {
      jobID: jobID,
      status: status,
      launched: launched,
      duration: duration
    };

    return CommonActions.deepEqual(thisRow, selectedRow);
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
    const timeDiff = duration ? `${moment.duration(endTime.diff(launchTime)).asSeconds()} seconds` : "Not available";

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
      <div className={`monitor-job-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="monitor-job-checkbox"><input type="checkbox" /></div>
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
  onClick: PropTypes.func,
  selectedRow: PropTypes.object,
  onClickLogs: PropTypes.func
};

MonitorJobTableRow.defaultProps = {
  jobID: "Invalid job ID",
  status: "Missing",
  launched: "Missing",
  duration: "Missing",
  onClick: () => {},
  selectedRow: {},
  onClickLogs: () => {}
};


export default MonitorJobTableRow;
