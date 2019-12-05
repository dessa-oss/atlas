import React from "react";
import moment from "moment";
import {
  get, put, del, delAtlas, patch
} from "./BaseActions";
import MonitorListTableRow from "../components/PackagePage/MonitorSchedules/MonitorListTableRow";
import MonitorJobTableRow from "../components/PackagePage/MonitorSchedules/MonitorJobTableRow";

const MonitorSchedulesActions = {
  getMonitorList: projectName => {
    const url = `projects/${projectName}/monitors`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return {};
      });
  },

  getRows: (results, onClickRow) => {
    const allMonitors = Object.keys(results);
    return allMonitors.map(monitor => {
      const key = results[monitor].properties.job_id + results[monitor].properties.metadata.username;
      return (
        <MonitorListTableRow
          key={key}
          onClick={onClickRow}
          monitorName={monitor}
          // Should add monitor name (without project prefix) to this payload in REST API later
          monitorNameLabel={results[monitor].properties.spec.environment.MONITOR_NAME}
          status={results[monitor].status}
          user={results[monitor].properties.metadata.username}
        />
      );
    });
  },

  getMonitorJobs: (projectName, monitorName, isAscending) => {
    const sortkind = (isAscending ? "asc" : "desc");
    console.log("Before request: ", isAscending, sortkind);
    const url = `projects/${projectName}/monitors/${monitorName}/jobs?sort=${sortkind}`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return {};
      });
  },

  getMonitorJobRows: (results, onSelectRow, toggleLogsModal) => {
    if (!results.error) {
      return results.map(job => {
        const key = job.job_id + job.duration;
        return (
          <MonitorJobTableRow
            key={key}
            jobID={job.job_id}
            status={job.status}
            completed={job.completed_time}
            started={job.start_time}
            onSelect={onSelectRow}
            onClickLogs={toggleLogsModal}
          />
        );
      });
    }
  },

  resumeMonitor: (projectName, monitorName) => {
    const body = {
      status: "active"
    };

    return put(
      `projects/${projectName}/monitors/${monitorName}`,
      body
    );
  },

  pauseMonitor: (projectName, monitorName) => {
    const body = {
      status: "pause"
    };

    return put(
      `projects/${projectName}/monitors/${monitorName}`,
      body
    );
  },

  deleteMonitor: (projectName, monitorName) => {
    return del(`projects/${projectName}/monitors/${monitorName}`);
  },

  updateMonitorSchedule: (projectName, monitorName, scheduleBody) => {
    const url = `projects/${projectName}/monitors/${monitorName}`;
    const body = {
      schedule: scheduleBody
    };
    return patch(url, body);
  },

  getScheduleRepeatValueOptions: scheduleRepeatUnit => {
    switch (scheduleRepeatUnit) {
      case "year":
        return [
          { label: "January", value: "1" },
          { label: "February", value: "2" },
          { label: "March", value: "3" },
          { label: "April", value: "4" },
          { label: "May", value: "5" },
          { label: "June", value: "6" },
          { label: "July", value: "7" },
          { label: "August", value: "8" },
          { label: "September", value: "9" },
          { label: "October", value: "10" },
          { label: "November", value: "11" },
          { label: "December", value: "12" }
        ];
      case "month":
        return [
          { label: "1st", value: "1" },
          { label: "2nd", value: "2" },
          { label: "3rd", value: "3" },
          { label: "4th", value: "4" },
          { label: "5th", value: "5" },
          { label: "6th", value: "6" },
          { label: "7th", value: "7" },
          { label: "8th", value: "8" },
          { label: "9th", value: "9" },
          { label: "10th", value: "10" },
          { label: "11th", value: "11" },
          { label: "12th", value: "12" },
          { label: "13th", value: "13" },
          { label: "14th", value: "14" },
          { label: "15th", value: "15" },
          { label: "16th", value: "16" },
          { label: "17th", value: "17" },
          { label: "18th", value: "18" },
          { label: "19th", value: "19" },
          { label: "20th", value: "20" },
          { label: "21st", value: "21" },
          { label: "22nd", value: "22" },
          { label: "23rd", value: "23" },
          { label: "24th", value: "24" },
          { label: "25th", value: "25" },
          { label: "26th", value: "26" },
          { label: "27th", value: "27" },
          { label: "28th", value: "28" },
          { label: "29th", value: "29" },
          { label: "30th", value: "30" },
          { label: "31st", value: "31" },
          { label: "last day of month", value: "last" }
        ];
      case "week":
        return [
          { label: "Monday", value: "0" },
          { label: "Tuesday", value: "1" },
          { label: "Wednesday", value: "2" },
          { label: "Thursday", value: "3" },
          { label: "Friday", value: "4" },
          { label: "Saturday", value: "5" },
          { label: "Sunday", value: "6" }
        ];
      case "day":
        return [
          { label: "12AM", value: "0" },
          { label: "1AM", value: "1" },
          { label: "2AM", value: "2" },
          { label: "3AM", value: "3" },
          { label: "4AM", value: "4" },
          { label: "5AM", value: "5" },
          { label: "6AM", value: "6" },
          { label: "7AM", value: "7" },
          { label: "8AM", value: "8" },
          { label: "9AM", value: "9" },
          { label: "10AM", value: "10" },
          { label: "11AM", value: "11" },
          { label: "12PM", value: "12" },
          { label: "1PM", value: "13" },
          { label: "2PM", value: "14" },
          { label: "3PM", value: "15" },
          { label: "4PM", value: "16" },
          { label: "5PM", value: "17" },
          { label: "6PM", value: "18" },
          { label: "7PM", value: "19" },
          { label: "8PM", value: "20" },
          { label: "9PM", value: "21" },
          { label: "10PM", value: "22" },
          { label: "11PM", value: "23" }
        ];
      case "hour":
        return [...Array(60).keys()].map(n => ({ label: `${n}m`, value: n.toString() }));
      case "minute":
        return [...Array(60).keys()].map(n => ({ label: `${n}s`, value: n.toString() }));
      default:
        return [];
    }
  },

  getSchedule: (
    startDate, endDate, scheduleRepeatUnit, scheduleRepeatValue
  ) => {
    const startMoment = moment(startDate);
    const startHour = startMoment.hours();
    const startMinute = startMoment.minutes();

    const schedule = {
      start_date: startMoment,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      month: "*",
      day: "*",
      hour: "*",
      minute: "*",
      second: "*"
    };

    switch (scheduleRepeatUnit) {
      case "year":
        schedule.month = scheduleRepeatValue.join(",");
        schedule.day = startMoment.date();
        schedule.hour = startHour;
        schedule.minute = startMinute;
        schedule.second = "0";
        break;
      case "month":
        schedule.day = scheduleRepeatValue.join(",");
        schedule.hour = startHour;
        schedule.minute = startMinute;
        schedule.second = "0";
        break;
      case "week":
        schedule.hour = startHour;
        schedule.minute = startMinute;
        schedule.second = "0";
        schedule.day_of_week = scheduleRepeatValue.join(",");
        delete schedule.day;
        break;
      case "day":
        schedule.hour = scheduleRepeatValue.join(",");
        schedule.minute = startMinute;
        schedule.second = "0";
        break;
      case "hour":
        schedule.minute = scheduleRepeatValue.join(",");
        schedule.second = "0";
        break;
      case "minute":
        schedule.second = scheduleRepeatValue.join(",");
        break;
      default:
        break;
    }

    if (endDate) {
      const endMoment = moment(endDate);
      schedule.end_date = endMoment;
    }

    return schedule;
  },

  parseSchedule: schedule => {
    let scheduleRepeatUnit = null;
    let scheduleRepeatValue = [];
    let scheduleArrayKey = null;
    if (schedule.day_of_week !== "*") {
      scheduleRepeatUnit = "week";
      scheduleArrayKey = "day_of_week";
    } else if (schedule.month !== "*") {
      scheduleRepeatUnit = "year";
      scheduleArrayKey = "month";
    } else if (schedule.day !== "*") {
      scheduleRepeatUnit = "month";
      scheduleArrayKey = "day";
    } else if (schedule.hour !== "*") {
      scheduleRepeatUnit = "day";
      scheduleArrayKey = "hour";
    } else if (schedule.minute !== "*") {
      scheduleRepeatUnit = "hour";
      scheduleArrayKey = "minute";
    } else if (schedule.second !== "*") {
      scheduleRepeatUnit = "minute";
      scheduleArrayKey = "second";
    }
    if (scheduleArrayKey !== null) {
      const scheduleRepeatValueArray = schedule[scheduleArrayKey].split(",");
      const toObjectMap = MonitorSchedulesActions.getScheduleRepeatValueOptions(scheduleRepeatUnit);
      scheduleRepeatValue = scheduleRepeatValueArray.map(
        value => toObjectMap.filter(object => object.value === value)[0]
      );
    }
    return { repeatUnit: scheduleRepeatUnit, repeatValue: scheduleRepeatValue };
  },

  deleteMonitorJobs: async (jobs, projectName, monitorName) => {
    const atlasPromises = Array.from(jobs).map(jobID => {
      const URL = `projects/${projectName}/job_listing/${jobID}`;
      return delAtlas(URL);
    });
    const orbitPromises = Array.from(jobs).map(jobID => {
      const URL = `projects/${projectName}/monitors/${monitorName}/jobs?job_id=${jobID}`;
      return del(URL);
    });
    await Promise.all(atlasPromises.concat(orbitPromises));
  }
};

export default MonitorSchedulesActions;
