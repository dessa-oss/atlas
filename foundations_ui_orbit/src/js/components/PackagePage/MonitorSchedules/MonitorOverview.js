import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import Select from "react-select";
import moment from "moment";
import Flatpickr from "react-flatpickr";
import CommonActions from "../../../actions/CommonActions";

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
    this.onChangeTimeEnd = this.onChangeTimeEnd.bind(this);
    this.onChangeScheduleRepeatUnit = this.onChangeScheduleRepeatUnit.bind(this);
    this.onChangeScheduleRepeatValue = this.onChangeScheduleRepeatValue.bind(this);

    let calDateStart = new Date();
    if (monitorResult.schedule.start_date) {
      calDateStart = new Date(monitorResult.schedule.start_date);
    }

    let calDateEnd = new Date();
    if (monitorResult.schedule.end_date) {
      calDateEnd = new Date(monitorResult.schedule.end_date);
    }

    this.state = {
      calDateStart: calDateStart,
      calDateEnd: calDateEnd,
      scheduleRepeatUnit: null,
      scheduleRepeatValue: [],
      scheduleValid: false
    };
  }

  async reload() {
    const { reload, monitorResult } = this.props;
    const result = MonitorSchedulesActions.parseSchedule(monitorResult.schedule);

    let calDateStart = new Date();
    if (monitorResult.schedule.start_date) {
      calDateStart = new Date(monitorResult.schedule.start_date);
    }

    let calDateEnd = new Date();
    if (monitorResult.schedule.end_date) {
      calDateEnd = new Date(monitorResult.schedule.end_date);
    }

    this.setState({
      calDateStart: calDateStart,
      calDateEnd: calDateEnd,
      scheduleRepeatUnit: result.repeatUnit,
      scheduleRepeatValue: result.repeatValue
    }, () => {
      this.setState({ scheduleValid: this.validateMonitorSchedule() }, reload);
    });
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    const { monitorResult } = this.props;

    if (!CommonActions.deepEqual(prevProps.monitorResult, monitorResult)) {
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
    const { toggleDeleteModal } = this.props;
    toggleDeleteModal();
  }

  updateMonitorSchedule() {
    const { monitorResult } = this.props;
    const {
      calDateStart,
      calDateEnd,
      scheduleRepeatUnit,
      scheduleRepeatValue
    } = this.state;

    const scheduleBody = MonitorSchedulesActions.getSchedule(
      calDateStart, calDateEnd,
      scheduleRepeatUnit, scheduleRepeatValue.map(obj => obj.value)
    );

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
    const { calDateStart } = this.state;

    calDateStart.setHours(time[0].getHours(), time[0].getMinutes(), 0, 0);

    this.setState({
      calDateStart: calDateStart
    }, () => {
      this.setState({ scheduleValid: this.validateMonitorSchedule() });
    });
  }

  onChangeTimeEnd(time) {
    const { calDateEnd } = this.state;

    calDateEnd.setHours(time[0].getHours(), time[0].getMinutes(), 0, 0);

    this.setState({
      calDateEnd: calDateEnd
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
    const {
      calDateStart,
      calDateEnd,
      scheduleRepeatUnit,
      scheduleRepeatValue
    } = this.state;
    const startTime = moment(calDateStart);
    const endTime = moment(calDateEnd);

    return (!calDateEnd || (startTime.isBefore(endTime) && endTime.isAfter(moment())))
    && scheduleRepeatUnit !== null && scheduleRepeatValue.length !== 0;
  }

  onChangeScheduleRepeatUnit(value) {
    const { scheduleRepeatUnit } = this.state;
    const newScheduleRepeatUnit = value.value;

    if (scheduleRepeatUnit !== newScheduleRepeatUnit) {
      this.setState({ scheduleRepeatUnit: newScheduleRepeatUnit, scheduleRepeatValue: [] },
        () => this.setState({ scheduleValid: this.validateMonitorSchedule() }));
    }
  }

  onChangeScheduleRepeatValue(value) {
    this.setState({ scheduleRepeatValue: value },
      () => this.setState({ scheduleValid: this.validateMonitorSchedule() }));
  }

  render() {
    const { monitorResult } = this.props;
    const {
      calDateStart,
      calDateEnd,
      scheduleRepeatUnit,
      scheduleRepeatValue,
      scheduleValid
    } = this.state;

    const status = monitorResult.status.split("")[0].toUpperCase() + monitorResult.status.slice(1);

    const scheduleOptions = [
      { label: "year", value: "year" },
      { label: "month", value: "month" },
      { label: "week", value: "week" },
      { label: "day", value: "day" },
      { label: "hour", value: "hour" },
      { label: "minute", value: "minute" }
    ];

    const clockTimeStart = `${calDateStart.getHours()}:${calDateStart.getMinutes()}`;
    const clockTimeEnd = `${calDateEnd.getHours()}:${calDateEnd.getMinutes()}`;

    const saveDisabled = !scheduleValid ? "disabled" : "";

    const nextRunTimes = (
      <div className="monitor-overview-value">
        {monitorResult.next_run_time.map((runTime, index) => (
          // eslint-disable-next-line react/no-array-index-key
          <div key={index} className="monitor-overview-runtime">
            {runTime ? moment.unix(runTime).format("YYYY-MM-DD HH:mm:ss") : "N/A"}
          </div>
        ))}
      </div>
    );

    const scheduleRepeatUnitOption = scheduleRepeatUnit ? { label: scheduleRepeatUnit } : null;

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
              <div className="monitor-overview-key">Next Run:</div>
              {nextRunTimes}
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
            <li className="monitor-overview-schedule">
              <div className="monitor-overview-key">Repeat every</div>
              <div className="monitor-overview-value">
                <Select
                  options={scheduleOptions}
                  className="react-select"
                  value={scheduleRepeatUnitOption}
                  onChange={this.onChangeScheduleRepeatUnit}
                />
                <p>on</p>
                <Select
                  defaultValue=""
                  options={MonitorSchedulesActions.getScheduleRepeatValueOptions(scheduleRepeatUnit)}
                  className="react-select-multi"
                  value={scheduleRepeatValue}
                  onChange={this.onChangeScheduleRepeatValue}
                  isMulti
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Starting on</div>
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
                  value={clockTimeStart}
                  className="schedule-flatpickr"
                  onChange={this.onChangeTimeStart}
                  options={{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    defaultDate: clockTimeStart,
                    time_24hr: true
                  }}
                />
              </div>
            </li>
            <li>
              <div className="monitor-overview-key">Ending on</div>
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
                <p> at </p>
                <Flatpickr
                  value={clockTimeEnd}
                  className="schedule-flatpickr"
                  onChange={this.onChangeTimeEnd}
                  options={{
                    enableTime: true,
                    noCalendar: true,
                    dateFormat: "H:i",
                    defaultDate: clockTimeEnd,
                    time_24hr: true
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
  reload: PropTypes.func,
  toggleDeleteModal: PropTypes.func
};

MonitorOverview.defaultProps = {
  monitorResult: {},
  reload: () => {},
  toggleDeleteModal: () => {}
};

export default MonitorOverview;
