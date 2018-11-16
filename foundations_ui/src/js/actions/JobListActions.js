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

  static isFieldHidden(hiddenArray, field) {
    return hiddenArray.includes(field);
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

  static getDurationClass(desiredTime, days, hours, minutes, seconds, isError) {
    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    let showingDays = false;
    let showingHours = false;
    let showingMinutes = false;

    const letterClass = isError ? 'font-regular error' : 'font-regular';

    if (days !== 0) {
      showingDays = true;
      const numberClass = isError
        ? 'duration-day-number  font-bold error'
        : 'duration-day-number  font-bold';
      daysUI = <span className={numberClass}>{days}<span className={letterClass}>d </span></span>;
    }

    const hourClass = isError
      ? 'duration-hour-number  font-bold error'
      : 'duration-hour-number  font-bold';
    if (hours !== 0) {
      showingHours = true;
      hoursUI = <span className={hourClass}>{hours}<span className={letterClass}>h </span></span>;
    } else if (showingDays) {
      hoursUI = <span className={hourClass}>0<span className={letterClass}>h </span></span>;
    }

    const minuteClass = isError
      ? 'duration-minute-number  font-bold error'
      : 'duration-minute-number  font-bold';
    if (minutes !== 0) {
      showingMinutes = true;
      minutesUI = <span className={minuteClass}>{minutes}<span className={letterClass}>m </span></span>;
    } else if (showingDays || showingHours) {
      minutesUI = <span className={minuteClass}>0<span className={letterClass}>m </span></span>;
    }

    const secondClass = isError
      ? 'duration-second-number  font-bold error'
      : 'duration-second-number  font-bold';
    if (seconds !== 0) {
      secondsUI = <span className={secondClass}>{seconds}<span className={letterClass}>s</span></span>;
    } else if (showingDays || showingHours || showingMinutes) {
      secondsUI = <span className={secondClass}>0<span className={letterClass}>s</span></span>;
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

  static getAllInputParams(allJobs) {
    const allInputParams = [];
    allJobs.forEach((job) => {
      job.input_params.forEach((input) => {
        if (input.value.type === 'constant') {
          if (!allInputParams.includes(input.name)) {
            allInputParams.push(input.name);
          }
        }
      });
    });
    return allInputParams;
  }

  static getConstantInputParams(allInputParams) {
    const constantParams = [];
    allInputParams.forEach((input) => {
      if (input.value.type === 'constant') {
        constantParams.push(input);
      }
    });
    return constantParams;
  }

  static getInputParamValue(inputParam) {
    if (inputParam.value && inputParam.value.value && inputParam.value.type === 'constant') {
      return inputParam.value.value;
    }
    return 'not available';
  }

  static getJobColumnHeaderH4Class(isStatus) {
    if (isStatus === isStatusField) {
      return 'blue-border-bottom status-header';
    }
    return 'blue-border-bottom';
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
