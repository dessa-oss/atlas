import React from 'react';
import BaseActions from './BaseActions';

const second = 1000;
const minute = second * 60;
const hour = minute * 60;
const day = hour * 24;
const isStatusField = true;

class ProjectActions {
  // API Calls
  static getJobs(projectName) {
    const url = 'projects/'.concat(projectName).concat('/job_listing');
    return BaseActions.getFromAPI(url)
      .then((res) => {
        return res;
      });
  }

  // Helper Functions
  static getDateDiff(earlierTime, laterTime) {
    const earlierDate = new Date(earlierTime);
    let laterDate;
    if (laterTime != null) {
      laterDate = new Date(laterTime);
    } else {
      laterDate = new Date(Date.now());
    }
    return laterDate.getTime() - earlierDate.getTime();
  }

  static getFormatedDate(startTime) {
    if (startTime == null || startTime.length === 0) {
      return '';
    }
    // API Format is '2018-08-23T09:30:00'
    // Desired Format is 'YYYY/MM/DD'
    const onlyDate = startTime.split('T')[0];
    const formatedDate = onlyDate.replace(/-/g, '/');
    return formatedDate;
  }

  static getFormatedTime(startTime) {
    if (startTime == null || startTime.length === 0) {
      return '';
    }
    // API Format is '2018-08-23T09:30:00'
    // Desired Format is 'HH:mm:ss'
    return startTime.split('T')[1];
  }

  static getDurationDays(durationTime) {
    return Math.floor(durationTime / day);
  }

  static getDurationHours(durationTime) {
    const durationHours = durationTime % day;
    return Math.floor(durationHours / hour);
  }

  static getDurationMinutes(durationTime) {
    const durationMinutes = durationTime % hour;
    return Math.floor(durationMinutes / minute);
  }

  static getDurationSeconds(durationTime) {
    const durationSeconds = durationTime % minute;
    return Math.floor(durationSeconds / second);
  }

  static getStatusCircle(status) {
    let statusCircle = 'status-green';

    if (status.toLowerCase() === 'running') {
      statusCircle = 'status-yellow';
    } else if (status.toLowerCase() === 'error') {
      statusCircle = 'status-red';
    }

    return 'status '.concat(statusCircle);
  }

  static getDurationClass(desiredTime, days, hours, minutes, seconds) {
    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    let showingDays = false;
    let showingHours = false;
    let showingMinutes = false;

    if (days !== 0) {
      showingDays = true;
      daysUI = <span className="duration-day-number header-4 font-bold">{days}<span className="font-regular">d </span></span>;
    }

    if (hours !== 0) {
      showingHours = true;
      hoursUI = <span className="duration-hour-number header-4 font-bold">{hours}<span className="font-regular">h </span></span>;
    } else if (showingDays) {
      hoursUI = <span className="duration-hour-number header-4 font-bold">0<span className="font-regular">h </span></span>;
    }

    if (minutes !== 0) {
      showingMinutes = true;
      minutesUI = <span className="duration-minute-number header-4 font-bold">{minutes}<span className="font-regular">m </span></span>;
    } else if (showingDays || showingHours) {
      minutesUI = <span className="duration-minute-number header-4 font-bold">0<span className="font-regular">m </span></span>;
    }

    if (seconds !== 0) {
      secondsUI = <span className="duration-second-number header-4 font-bold">{seconds}<span className="font-regular">s</span></span>;
    } else if (showingDays || showingHours || showingMinutes) {
      secondsUI = <span className="duration-second-number header-4 font-bold">0<span className="font-regular">s</span></span>;
    }

    switch (desiredTime) {
      case 'days':
        return daysUI;
      case 'hours':
        return hoursUI;
      case 'minutes':
        return minutesUI;
      case 'seconds':
        return secondsUI;
      default:
        return null;
    }
  }

  static getJobColumnHeaderH4Class(isStatus) {
    if (isStatus === isStatusField) {
      return 'header-4 blue-border-bottom status-header';
    }
    return 'header-4 blue-border-bottom';
  }

  static getJobColumnHeaderArrowClass(isStatus) {
    if (isStatus === isStatusField) {
      return 'arrow-down margin-auto';
    }
    return 'arrow-down float-right';
  }

  static getTableSectionHeaderDivClass(header) {
    if (header !== '') {
      return 'table-section-header blue-header';
    }
    return 'table-section-header';
  }

  static getTableSectionHeaderArrowClass(header) {
    if (header !== '') {
      return 'arrow-down blue-header-arrow';
    }
    return '';
  }

  static getTableSectionHeaderTextClass(header) {
    if (header !== '') {
      return 'blue-header-text font-regular';
    }
    return 'blue-header-text font-regular no-margin';
  }
}

export default ProjectActions;
