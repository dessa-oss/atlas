import React from 'react';
import BaseActions from './BaseActions';

const second = 1000;
const minute = second * 60;
const hour = minute * 60;
const day = hour * 24;
const isStatusField = true;
const statusText = 'Status';

class ProjectActions {
  // API Calls
  static getJobs(projectName) {
    const url = this.getBaseJobListingURL(projectName);
    // TODO get Jobs is currently in Beta
    return BaseActions.getBetaFromAPI(url)
      .then((res) => {
        return res;
      });
  }

  static filterJobs(projectName, statusFilter) {
    if (!this.areStatusesHidden(statusFilter)) {
      return this.getJobs(projectName);
    }

    let url = this.getBaseJobListingURL(projectName);
    const filterURL = this.getFilterURL(statusFilter);
    url = url.concat('?').concat(filterURL);

    // TODO get Jobs is currently in Beta
    return BaseActions.getBetaFromAPI(url)
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

    if (status.toLowerCase() === 'running' || status.toLowerCase() === 'processing') {
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

    const letterClass = isError ? 'error' : '';
    const numberClass = isError
      ? 'font-bold error'
      : 'font-bold';
    if (days !== 0) {
      showingDays = true;
      daysUI = <span className={numberClass}>{days}<span className={letterClass}>d </span></span>;
    }

    if (hours !== 0) {
      showingHours = true;
      hoursUI = <span className={numberClass}>{hours}<span className={letterClass}>h </span></span>;
    } else if (showingDays) {
      hoursUI = <span className={numberClass}>0<span className={letterClass}>h </span></span>;
    }

    if (minutes !== 0) {
      showingMinutes = true;
      minutesUI = <span className={numberClass}>{minutes}<span className={letterClass}>m </span></span>;
    } else if (showingDays || showingHours) {
      minutesUI = <span className={numberClass}>0<span className={letterClass}>m </span></span>;
    }

    if (seconds !== 0) {
      secondsUI = <span className={numberClass}>{seconds}<span className={letterClass}>s</span></span>;
    } else if (showingDays || showingHours || showingMinutes) {
      secondsUI = <span className={numberClass}>0<span className={letterClass}>s</span></span>;
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
        if (!allInputParams.includes(input.name)) {
          allInputParams.push(input.name);
        }
      });
    });
    return allInputParams;
  }

  static getConstantInputParams(allInputParams) {
    const constantParams = [];
    allInputParams.forEach((input) => {
      constantParams.push(input);
    });
    return constantParams;
  }

  static getInputMetricValue(inputParam, isMetric, columns) {
    if (isMetric && inputParam !== null && inputParam.value) {
      return inputParam.value;
    }

    if (inputParam && columns.includes(inputParam.name)
    && inputParam.value) {
      return inputParam.value;
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
      return 'arrow-down';
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
      return 'blue-header-text';
    }
    return 'blue-header-text no-margin';
  }

  static getAllMetrics(allJobs) {
    return (this.getAllMetricsFromJobs(allJobs));
  }

  static getFilterURL(statusFilter) {
    let url = '';
    let isFirstStatus = true;
    statusFilter.forEach((status) => {
      url = this.addToURLNotHidden(url, isFirstStatus, status);
      isFirstStatus = this.setIsFirst(status, isFirstStatus);
    });

    return url;
  }

  static getBaseJobListingURL(projectName) {
    return 'projects/'.concat(projectName).concat('/job_listing');
  }

  static areStatusesHidden(statuses) {
    const areHidden = statuses.some((status) => {
      return (status.hidden === true);
    });
    return areHidden;
  }

  static getAllFilters(oldFilters, statuses) {
    return this.getStatusFilters(oldFilters, statuses);
  }

  static getStatusFilters(oldFilters, statuses) {
    const newFilters = this.getOldStatusFilters(oldFilters);
    this.addNewStatusFilters(statuses, newFilters);
    return newFilters;
  }

  static removeFilter(oldFilters, removeFilter) {
    const newFilters = [];
    oldFilters.forEach((filter) => {
      if (!this.doesFilterExist(filter, removeFilter)) {
        newFilters.push(filter);
      }
    });
    return newFilters;
  }

  static getUpdatedStatuses(oldStatuses, filters) {
    const newStatuses = [];
    let noStatusFilters = true;
    oldStatuses.forEach((status) => {
      this.getUpdatedStatusesFromOldStatuses(filters, status, noStatusFilters, newStatuses);
    });

    this.updateStatusesIfNoFilters(noStatusFilters, newStatuses);

    return newStatuses;
  }

  static updateStatusesIfNoFilters(noStatusFilters, newStatuses) {
    if (noStatusFilters) {
      newStatuses.forEach((status) => {
        status.hidden = false;
      });
    }
  }

  static addToURLNotHidden(url, isFirstStatus, status) {
    let newUrl = '';
    if (status.hidden === false) {
      newUrl = this.addToURL(url, isFirstStatus, status);
    }
    return newUrl;
  }

  static addToURL(url, isFirstStatus, status) {
    let newURL = url;
    if (isFirstStatus) {
      newURL += 'status='.concat(status.name);
    } else {
      newURL += ','.concat(status.name);
    }
    return newURL;
  }

  static getFilterObject(columnName, value) {
    return { column: columnName, value };
  }

  static doesFilterExist(oldFilter, newFilter) {
    return oldFilter.column === newFilter.column && oldFilter.value === newFilter.value;
  }

  static setIsFirst(status, isFirstStatus) {
    let returnStatus = isFirstStatus;
    if (status.hidden === false) {
      returnStatus = false;
    }
    return returnStatus;
  }

  static getOldStatusFilters(oldFilters) {
    return oldFilters.filter(
      (filter) => {
        if (filter.column !== statusText) {
          return filter;
        }
      },
    );
  }

  static addNewStatusFilters(statuses, newFilters) {
    if (this.areStatusesHidden(statuses)) {
      statuses.forEach((status) => {
        if (status.hidden === false) {
          const newFilter = this.getFilterObject(statusText, status.name);
          newFilters.push(newFilter);
        }
      });
    }
  }

  static getUpdatedStatusesFromOldStatuses(filters, status, noStatusFilters, newStatuses) {
    const statusInFilter = this.getFilterObject(statusText, status.name);
    let isHidden = true;
    filters.forEach((filter) => {
      if (this.doesFilterExist(filter, statusInFilter)) {
        isHidden = false;
        noStatusFilters = false;
      }
    });
    newStatuses.push({ name: status.name, hidden: isHidden });
  }

  // private fun

  static getAllMetricsFromJobs(allJobs) {
    const allMetrics = [];
    allJobs.forEach((job) => {
      if (job.output_metrics) {
        job.output_metrics.forEach((metric) => {
          if (!allMetrics.includes(metric.name)) {
            allMetrics.push(metric.name);
          }
        });
      }
    });
    return allMetrics;
  }
}

export default ProjectActions;
