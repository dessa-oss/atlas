import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";

class MonitorOverview extends Component {
  render() {
    const { monitorResult } = this.props;
    const nextRun = monitorResult.next_run_time ? monitorResult.next_run_time : "No next run specified";
    const status = monitorResult.status.split("")[0].toUpperCase() + monitorResult.status.slice(1, -1);

    return (
      <div className="monitor-info">
        <div className="monitor-overview">
          <h3>Overview</h3>
          <div className="monitor-overview-menu">
            <div className="i--icon-open" />
            <div className="i--icon-start" />
            <div className="i--icon-pause" />
            <div className="i--icon-delete" />
          </div>
          <ul>
            <li>
              <div className="monitor-overview-key">Monitor Name:</div>
              <div className="monitor-overview-value">{monitorResult.properties.job_id}</div>
            </li>
            <li>
              <div className="monitor-overview-key">Status:</div>
              <div className="monitor-overview-value">{status}</div>
            </li>
            <li>
              <div className="monitor-overview-key">User:</div>
              <div className="monitor-overview-value">{monitorResult.properties.metadata.username}</div>
            </li>
            <li>
              <div className="monitor-overview-key">Next Runs:</div>
              <div className="monitor-overview-value">{nextRun}</div>
            </li>
          </ul>
        </div>
        <div className="monitor-details">
          <h3>Schedule Details</h3>
          <ul>
            <li>
              <div className="monitor-overview-key">Repeats:</div>
              <div className="monitor-overview-value">
                <select className="schedule-picker" name="schedule-picker">
                  <option value="weekly">Weekly</option>
                  <option value="daily">Daily</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Starting on:</div>
              <div className="monitor-overview-value">Oct. 15 2020</div>
            </li>
            <li>
              <div className="monitor-overview-key">Ending on:</div>
              <div className="monitor-overview-value">Sept. 16 2020</div>
            </li>
          </ul>
        </div>
        {/* <div className="monitor-calendar">
          <h3>Calendar</h3>
        </div> */}
      </div>
    );
  }
}

MonitorOverview.propTypes = {
  monitorResult: PropTypes.object
};

MonitorOverview.defaultProps = {
  monitorResult: {}
};

export default MonitorOverview;
