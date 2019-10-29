import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import Select from "react-select";
import moment from "moment";
import Flatpickr from "react-flatpickr";
// import Calendar from "react-calendar";

class MonitorOverview extends Component {
  constructor(props) {
    super(props);

    const { monitorResult } = this.props;

    this.resumeMonitor = this.resumeMonitor.bind(this);
    this.pauseMonitor = this.pauseMonitor.bind(this);
    this.deleteMonitor = this.deleteMonitor.bind(this);
    this.updateMonitorSchedule = this.updateMonitorSchedule.bind(this);
    // this.changeEditMode = this.changeEditMode.bind(this);
    this.state = {
      calDate: monitorResult.schedule.start_date
        ? [monitorResult.schedule.start_date, monitorResult.schedule.end_date]
        : new Date(),
      calDateTimeEnd: monitorResult.schedule.end_date
        ? monitorResult.schedule.end_date.split(" ").slice(0, 4).join(" ")
        : "12:00"
    };
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

  updateMonitorSchedule() {
    const { monitorResult } = this.props;
    const { calDate } = this.state;
    const calStartDate = moment(calDate[0]).format("YYYY-MM-DD");
    const calEndDate = moment(calDate[1]).format("YYYY-MM-DD");

    const scheduleBody = {
      day: "*",
      day_of_week: "*",
      hour: "*",
      minute: "*",
      month: "*",
      second: "*/19",
      week: "*",
      year: "*",
      start_date: calStartDate,
      end_date: calEndDate
    };
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.updateMonitorSchedule(projectName, monitorName, scheduleBody);
  }

  // changeEditMode() {
  //   const { editMode } = this.state;
  //   this.setState(prevState => ({
  //     editMode: !prevState.editMode
  //   }));
  // }

  render() {
    const { monitorResult } = this.props;
    // const { editMode } = this.state;
    const { calDate, calDateTimeEnd } = this.state;
    const nextRun = monitorResult.next_run_time
      ? moment.unix(monitorResult.next_run_time).format("YYYY-MM-DD HH:mm:ss")
      : "None scheduled";

    const status = monitorResult.status.split("")[0].toUpperCase() + monitorResult.status.slice(1);

    const startTime = monitorResult.schedule.start_date ? monitorResult.schedule.start_date : "Not specified";
    const endTime = monitorResult.schedule.end_date ? monitorResult.schedule.end_date : "Not specified";

    const scheduleOptions = [
      { label: "Years", value: monitorResult.schedule.year },
      { label: "Months", value: monitorResult.schedule.month },
      { label: "Weeks", value: monitorResult.schedule.week },
      { label: "Days", value: monitorResult.schedule.day },
      { label: "Hours", value: monitorResult.schedule.hour },
      { label: "Minutes", value: monitorResult.schedule.minute },
      { label: "Seconds", value: monitorResult.schedule.second }
    ];

    function findScheduleRepeat(schedule) {
      for (let i = 0; i < schedule.length; i += 1) {
        if (schedule[i].value !== "*") {
          if (schedule[i].value.includes("/")) {
            return {
              label: schedule[i].label,
              value: schedule[i].value.split("/")[1]
            };
          }
          return schedule[i];
        }
      }
    }

    const defaultScheduleValue = findScheduleRepeat(scheduleOptions);

    const calStartTime = startTime.split(" ").slice(0, 4).join(" ");
    const calEndTime = endTime.split(" ").slice(0, 4).join(" ");

    const calStartTime2 = startTime.split(" ")[4];
    const calEndTime2 = endTime.split(" ")[4];

    const clockTimeHour = monitorResult.schedule.hour;
    const clockTimeMinute = monitorResult.schedule.minute;
    const clockTimeSecond = monitorResult.schedule.second;

    const clockTime = `${clockTimeHour}:${clockTimeMinute}:${clockTimeSecond}`;

    return (
      <div className="monitor-info">
        <div className="monitor-overview">
          <h3>Overview</h3>
          <div className="monitor-overview-menu">
            <div className="i--icon-start" onClick={this.resumeMonitor} />
            <div className="i--icon-pause" onClick={this.pauseMonitor} />
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
            <li>
              <div className="monitor-overview-key">Start Date:</div>
              <div className="monitor-overview-value">{calStartTime}</div>
            </li>
            <li>
              <div className="monitor-overview-key">End Date:</div>
              <div className="monitor-overview-value">{calEndTime}</div>
            </li>
          </ul>
        </div>
        <div className="monitor-details">
          <h3>Schedule Details</h3>
          {/* {findEditMode} */}
          <div>
            {/* <button type="button" onClick={this.changeEditMode} /> */}
          </div>
          <ul>
            <li>
              <div className="monitor-overview-key">Repeats every:</div>
              <div className="monitor-overview-value">
                <input
                  value={defaultScheduleValue.value}
                  className="monitor-repeat-value"
                  type="number"
                />
                <Select
                  options={scheduleOptions}
                  className="react-select"
                  defaultValue={defaultScheduleValue}
                />
                <p> at </p>
                <Flatpickr
                  value={clockTime}
                  className="schedule-flatpickr"
                  onChange={time => { this.setState({ calDateTimeEnd: time }); }}
                  options={{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    defaultDate: calStartTime2
                  }}
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Date range:</div>
              <div className="monitor-overview-value">
                <Flatpickr
                  value={calDate}
                  onChange={date => { this.setState({ calDate: date }); }}
                  options={{
                    altFormat: "F j, Y",
                    dateFormat: "Y-m-d",
                    defaultDate: [new Date(), "2020-10-30"],
                    mode: "range"
                  }}
                />
              </div>
            </li>
            <div className="monitor-details-options">
              <button onClick={this.updateMonitorSchedule} type="button">Save</button>
            </div>
          </ul>
        </div>
        <div className="monitor-calendar">
          <h3> </h3>
        </div>
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
