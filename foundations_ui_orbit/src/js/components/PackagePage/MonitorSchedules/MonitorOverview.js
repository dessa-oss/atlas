import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import Select from "react-select";
import moment from "moment";

class MonitorOverview extends Component {
  constructor(props) {
    super(props);

    this.resumeMonitor = this.resumeMonitor.bind(this);
    this.pauseMonitor = this.pauseMonitor.bind(this);
    this.deleteMonitor = this.deleteMonitor.bind(this);
  }

  resumeMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.resumeMonitor(projectName, monitorName);
  }

  pauseMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.pauseMonitor(projectName, monitorName);
  }

  deleteMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.deleteMonitor(projectName, monitorName);
  }

  render() {
    const { monitorResult } = this.props;
    const nextRun = monitorResult.next_run_time
      ? moment.unix(monitorResult.next_run_time).format("YYYY-MM-DD MM:SS")
      : "None scheduled";

    const status = monitorResult.status.split("")[0].toUpperCase() + monitorResult.status.slice(1);

    const startTime = monitorResult.schedule.start_date ? monitorResult.schedule.start_date : "Not specified";
    const endTime = monitorResult.schedule.end_date ? monitorResult.schedule.end_date : "Not specified";

    const scheduleOptions = [
      { label: "Year", value: monitorResult.schedule.year },
      { label: "Month", value: monitorResult.schedule.month },
      { label: "Week", value: monitorResult.schedule.week },
      { label: "Day", value: monitorResult.schedule.day },
      { label: "Hour", value: monitorResult.schedule.hour },
      { label: "Minute", value: monitorResult.schedule.minute },
      { label: "Second", value: monitorResult.schedule.second }
    ];

    function findScheduleRepeat(schedule) {
      const repeatOn = Object.keys(schedule).filter(timeFrame => {
        return schedule[timeFrame] && schedule[timeFrame].toString().includes("/");
      });
      const jobHasSchedule = repeatOn[0];
      if (jobHasSchedule) {
        const formattedKey = repeatOn[0][0].toUpperCase() + repeatOn[0].slice(1);
        return scheduleOptions.filter(timeFrame => timeFrame.label === formattedKey)[0];
      }
    }

    const defaultScheduleValue = findScheduleRepeat(monitorResult.schedule);

    return (
      <div className="monitor-info">
        <div className="monitor-overview">
          <h3>Overview</h3>
          <div className="monitor-overview-menu">
            <div className="i--icon-open" />
            <div className="i--icon-start" onClick={this.resumeMonitor} />
            <div className="i--icon-pause" onClick={this.pauseMonitor} />
            {/* <div className="i--icon-delete" onClick={this.deleteMonitor} /> */}
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
              <div className="monitor-overview-key">Repeats every:</div>
              <div className="monitor-overview-value">
                <Select
                  options={scheduleOptions}
                  className="react-select"
                  defaultValue={defaultScheduleValue}
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Starting on:</div>
              <div className="monitor-overview-value">{
                startTime.split("2019")[0]}, at {startTime.split("2019")[1]}
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Ending on:</div>
              <div className="monitor-overview-value">{endTime}</div>
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
