import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import Select from "react-select";
import moment from "moment";
import Flatpickr from "react-flatpickr";

class MonitorOverview extends Component {
  constructor(props) {
    super(props);

    const { monitorResult } = this.props;

    this.resumeMonitor = this.resumeMonitor.bind(this);
    this.pauseMonitor = this.pauseMonitor.bind(this);
    this.deleteMonitor = this.deleteMonitor.bind(this);
    this.updateMonitorSchedule = this.updateMonitorSchedule.bind(this);
    this.reload = this.reload.bind(this);
    this.onChangeDateStart = this.onChangeDateStart.bind(this);
    this.onChangeTimeStart = this.onChangeTimeStart.bind(this);
    this.onChangeDateEnd = this.onChangeDateEnd.bind(this);

    this.state = {
      nextRunTime: monitorResult.next_run_time || "None set",
      calDateStart: monitorResult.schedule.start_date || new Date(),
      calDateEnd: monitorResult.schedule.end_date || "",
      clockTimeHour: new Date(monitorResult.schedule.start_date).getHours() || "12",
      clockTimeMinute: new Date(monitorResult.schedule.start_date).getMinutes() || "00",
      scheduleRepeatUnit: { label: "Days" },
      scheduleRepeatUnitValue: "1",
      scheduleValid: false
    };
  }

  findScheduleRepeat() {
    const { monitorResult } = this.props;

    const scheduleOptions = [
      { label: "Years", value: monitorResult.schedule.year },
      { label: "Months", value: monitorResult.schedule.month },
      { label: "Weeks", value: monitorResult.schedule.week },
      { label: "Days", value: monitorResult.schedule.day },
      { label: "Hours", value: monitorResult.schedule.hour },
      { label: "Minutes", value: monitorResult.schedule.minute },
      { label: "Seconds", value: monitorResult.schedule.second }
    ];

    for (let i = 0; i < scheduleOptions.length; i += 1) {
      if (scheduleOptions[i].value !== "*") {
        if (scheduleOptions[i].value.includes("/")) {
          return {
            label: scheduleOptions[i].label,
            value: scheduleOptions[i].value.split("/")[1]
          };
        }
        return scheduleOptions[i];
      }
    }
  }

  async reload() {
    const { reload, monitorResult } = this.props;
    const result = this.findScheduleRepeat();
    if (result) {
      this.setState({
        scheduleRepeatUnitValue: result.value,
        nextRunTime: moment.unix(monitorResult.next_run_time).format("YYYY-MM-DD HH:mm:ss") || "None set",
        calDateStart: monitorResult.schedule.start_date || new Date(),
        calDateEnd: monitorResult.schedule.end_date || "",
        clockTimeHour: new Date(monitorResult.schedule.start_date).getHours() || "12",
        clockTimeMinute: new Date(monitorResult.schedule.start_date).getMinutes() || "00",
        scheduleRepeatUnit: result
      }, () => {
        this.setState({ scheduleValid: this.validateMonitorSchedule() }, reload);
      });
    } else {
      reload();
    }
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

  resumeMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.resumeMonitor(projectName, monitorName).then(this.reload);
  }

  pauseMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.pauseMonitor(projectName, monitorName).then(this.reload);
  }

  deleteMonitor() {
    const { monitorResult } = this.props;
    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.deleteMonitor(projectName, monitorName).then(this.reload);
  }

  updateMonitorSchedule() {
    const { monitorResult } = this.props;
    const {
      calDateStart,
      calDateEnd,
      clockTimeHour,
      clockTimeMinute,
      scheduleRepeatUnit,
      scheduleRepeatUnitValue
    } = this.state;
    const calStartDate = moment(calDateStart).format("YYYY-MM-DD");

    const scheduleBody = {
      year: "*",
      month: "*",
      week: "*",
      day: "*",
      hour: "*",
      second: "*",
      start_date: `${calStartDate} ${clockTimeHour}:${clockTimeMinute}`
    };

    if (calDateEnd !== "") {
      scheduleBody.end_date = moment(calDateEnd).format("YYYY-MM-DD");
    }
    scheduleBody[scheduleRepeatUnit.label.toLocaleLowerCase().slice(0, -1)] = `*/${scheduleRepeatUnitValue}`;

    const projectName = monitorResult.properties.spec.environment.PROJECT_NAME;
    const monitorName = monitorResult.properties.spec.environment.MONITOR_NAME;
    MonitorSchedulesActions.updateMonitorSchedule(projectName, monitorName, scheduleBody).then(this.reload);
  }

  onChangeDateStart(date) {
    this.setState({ calDateStart: date[0] }, () => {
      this.setState({ scheduleValid: this.validateMonitorSchedule() });
    });
  }

  onChangeTimeStart(time) {
    this.setState({
      clockTimeHour: time[0].getHours(),
      clockTimeMinute: time[0].getMinutes()
    }, () => {
      this.setState({ scheduleValid: this.validateMonitorSchedule() });
    });
  }

  onChangeDateEnd(date) {
    this.setState({ calDateEnd: date[0] }, () => {
      this.setState({ scheduleValid: this.validateMonitorSchedule() });
    });
  }

  validateMonitorSchedule() {
    const { calDateStart, calDateEnd } = this.state;
    const startTime = moment(calDateStart);
    const endTime = moment(calDateEnd);

    return startTime.isBefore(endTime) && endTime.isAfter(moment());
  }

  render() {
    const { monitorResult } = this.props;
    const {
      calDateStart,
      calDateEnd,
      scheduleRepeatUnit,
      scheduleRepeatUnitValue,
      nextRunTime,
      scheduleValid
    } = this.state;

    const status = monitorResult.status.split("")[0].toUpperCase() + monitorResult.status.slice(1);

    const scheduleOptions = [
      { label: "Years", value: monitorResult.schedule.year },
      { label: "Months", value: monitorResult.schedule.month },
      { label: "Weeks", value: monitorResult.schedule.week },
      { label: "Days", value: monitorResult.schedule.day },
      { label: "Hours", value: monitorResult.schedule.hour },
      { label: "Minutes", value: monitorResult.schedule.minute },
      { label: "Seconds", value: monitorResult.schedule.second }
    ];

    const clockTimeDateObject = new Date(calDateStart);
    const clockTime = `${clockTimeDateObject.getHours()}:${clockTimeDateObject.getMinutes()}`;
    const saveDisabled = !scheduleValid ? "disabled" : "";

    return (
      <div className="monitor-info">
        <div className="monitor-overview">
          <h3>
            {monitorResult.properties.spec.environment.MONITOR_NAME}
          </h3>
          <div className="monitor-overview-menu">
            <button className="monitor-btn" type="button" onClick={this.resumeMonitor}>
              <div className="i--icon-start" />
            </button>
            <button className="monitor-btn" type="button" onClick={this.pauseMonitor}>
              <div className="i--icon-pause" />
            </button>
            <button className="monitor-btn" type="button" onClick={this.deleteMonitor}>
              <div className="i--icon-delete" />
            </button>
          </div>
          <ul>
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
              <div className="monitor-overview-value">{nextRunTime}</div>
            </li>
          </ul>
        </div>
        <div className="monitor-details">
          <h3>Schedule Details</h3>
          <div className="monitor-details-options">
            <button
              className={`save-schedule-btn ${saveDisabled}`}
              onClick={this.updateMonitorSchedule}
              type="button"
              disabled={!scheduleValid}
            >
              Save
            </button>
          </div>
          <ul>
            <li>
              <div className="monitor-overview-key">Repeats every:</div>
              <div className="monitor-overview-value">
                <input
                  value={scheduleRepeatUnitValue}
                  className="monitor-repeat-value"
                  type="number"
                  step="1"
                  min="0"
                  pattern="[0-9]"
                  onChange={value => {
                    this.setState({
                      scheduleRepeatUnitValue: value.target.value
                    });
                  }}
                />
                <Select
                  options={scheduleOptions}
                  className="react-select"
                  value={scheduleRepeatUnit}
                  onChange={value => {
                    this.setState({
                      scheduleRepeatUnit: value
                    });
                  }}
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Starting on:</div>
              <div className="monitor-overview-value">
                <Flatpickr
                  className="cal-picker"
                  value={calDateStart}
                  onChange={this.onChangeDateStart}
                  options={{
                    altFormat: "F j, Y",
                    dateFormat: "Y-m-d",
                    defaultDate: new Date()
                  }}
                />
                <p> at </p>
                <Flatpickr
                  value={clockTime}
                  className="schedule-flatpickr"
                  onChange={this.onChangeTimeStart}
                  options={{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    defaultDate: clockTime,
                    time_24hr: true
                  }}
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Ending on:</div>
              <div className="monitor-overview-value">
                <Flatpickr
                  className="cal-picker"
                  value={calDateEnd}
                  onChange={this.onChangeDateEnd}
                  options={{
                    altFormat: "F j, Y",
                    dateFormat: "Y-m-d"
                  }}
                />
              </div>
            </li>
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
  monitorResult: PropTypes.object,
  reload: PropTypes.func
};

MonitorOverview.defaultProps = {
  monitorResult: {},
  reload: () => {}
};

export default MonitorOverview;
