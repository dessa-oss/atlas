import React from 'react';
import BaseActions from './BaseActions';
import CommonActions from './CommonActions';

const second = 1000;
const minute = second * 60;
const hour = minute * 60;
const day = hour * 24;
const isStatusField = true;
const statusText = 'Status';

class JobListActions {
  // API Calls
  static getJobs(projectName) {
    const url = this.getBaseJobListingURL(projectName);
    // TODO get Jobs is currently in Beta
    return BaseActions.getBetaFromAPI(url)
      .then(([status, result]) => {
        return {
          status,
          result,
        };
      });
  }

  static filterJobs(
    projectName, statusFilter, userFilter, numberFilters, containFilters, boolFilters, durationFilters, jobIdFilters,
    startTimeFilters,
  ) {
    // if no filters just get regular jobs
    if (this.areNoFilters(statusFilter, userFilter, numberFilters, containFilters, boolFilters, durationFilters,
      jobIdFilters, startTimeFilters)) {
      return this.getJobs(projectName);
    }

    let url = this.getBaseJobListingURL(projectName);
    const filterURL = this.getFilterURL(
      statusFilter, userFilter, numberFilters, containFilters, boolFilters, durationFilters, jobIdFilters,
      startTimeFilters,
    );
    url = url.concat('?').concat(filterURL);

    // TODO get Jobs is currently in Beta
    return BaseActions.getBetaFromAPI(url)
      .then(([status, result]) => {
        return {
          status,
          result,
        };
      });
  }

  // Helper Functions
  static parseDuration(duration) {
    if (!duration) return 0;

    const oneSecond = 1000;
    const match = duration.match(/(\d+)d(\d+)h(\d+)m(\d+)s/);
    const secondDuration = parseInt(match[1], 10) * 86400
      + parseInt(match[2], 10) * 3600
      + parseInt(match[3], 10) * 60
      + parseInt(match[4], 10);
    const millisecondDuration = secondDuration * oneSecond;

    return millisecondDuration || 1000;
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
    // Desired Format is 'HH:mm:ss AM/PM'
    const newDate = new Date(startTime);
    return `${CommonActions.formatAMPM(newDate)} EST`;
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

    if (status.toLowerCase() === 'queued') {
      statusCircle = 'status-yellow';
    } else if (status.toLowerCase() === 'running') {
      statusCircle = 'status-running';
    } else if (CommonActions.isError(status)) {
      statusCircle = 'status-red';
    }

    return 'status-icon '.concat(statusCircle);
  }

  static getDurationClass(desiredTime, days, hours, minutes, seconds, isError) {
    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    let showingDays = false;
    let showingHours = false;
    let showingMinutes = false;

    const letterClass = CommonActions.errorStatus(isError);
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

  static getConstantInputParams(allInputParams) {
    const constantParams = [];
    allInputParams.forEach((input) => {
      constantParams.push(input);
    });
    return constantParams;
  }

  static roundToSigFigs(number, precision) {
    let value = number.toString();

    if (value.length >= precision + 1) {
      value = number.toExponential(precision - 1);
    }

    if (value.endsWith('e+0')) {
      value = value.slice(0, -3);
    }

    return value;
  }

  static roundToSigFigsIfNumber(value, precision) {
    if (typeof value === 'number') {
      return this.roundToSigFigs(value, precision);
    }
    return value;
  }

  static isValidMetricValue(isMetric, inputParam) {
    return isMetric && inputParam !== null && inputParam.value !== null;
  }

  static isValidParameter(inputParam, columns) {
    return inputParam && columns.includes(inputParam.name) && inputParam.value !== null;
  }

  static getInputMetricValue(inputParam, isMetric, columns) {
    if (this.isValidMetricValue(isMetric, inputParam) || this.isValidParameter(inputParam, columns)) {
      return this.roundToSigFigsIfNumber(inputParam.value, 5);
    }
    return 'not available';
  }

  static getJobColumnHeaderH4Class(isStatus) {
    if (isStatus === isStatusField) {
      return 'status-header';
    }
    return '';
  }

  static getJobColumnHeaderArrowClass(isStatus, colType, isMetric) {
    let metricClass = 'not-metric';
    if (isMetric) {
      metricClass = 'is-metric';
    }

    if (isStatus === isStatusField) {
      return 'arrow-down'.concat(' ').concat(colType).concat(' ').concat(metricClass);
    }
    return 'arrow-down float-right'.concat(' ').concat(colType).concat(' ').concat(metricClass);
  }

  static getJobColumnHeaderDivClass(containerDivClass, isStatus) {
    let divClass = containerDivClass;
    if (isStatus) {
      divClass += ' status-header';
    }
    return divClass;
  }

  static getJobColumnHeaderPresentationClass(colType, isMetric) {
    let metricClass = 'not-metric';
    if (isMetric) {
      metricClass = 'is-metric';
    }

    return 'arrow-container '.concat(colType).concat(' ').concat(metricClass);
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

  static getFilterURL(
    statusFilter, userFilter, numberFilters, containFilters, boolFilters, durationFilters, jobIdFilters,
    startTimeFilters,
  ) {
    let url = '';
    let isFirstFilter = true;
    if (this.areStatusesHidden(statusFilter)) {
      let isFirstStatus = true;
      statusFilter.forEach((status) => {
        url = this.addStatusToURLNotHidden(url, isFirstStatus, status);
        isFirstStatus = this.setIsFirst(status, isFirstStatus);
      });
      isFirstFilter = false;
    }
    let isFirstUser = true;
    if (userFilter.length > 0) {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
    }
    userFilter.forEach((user) => {
      url = this.addToURLNotHidden(url, isFirstUser, user, 'user');
      isFirstUser = false;
      isFirstFilter = false;
    });

    numberFilters.forEach((numberFilter) => {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
      url = this.addToURLRangeNotHidden(url, numberFilter.min, numberFilter.max, numberFilter.columnName);
      isFirstFilter = false;
    });

    containFilters.forEach((containFilter) => {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
      url = this.addToURLContainFilter(url, containFilter.searchText, containFilter.columnName);
      isFirstFilter = false;
    });

    if (this.boolFilterArrayHasHidden(boolFilters)) {
      boolFilters.forEach((boolFilter) => {
        if (this.boolFilterHasHidden(boolFilter)) {
          const nonHiddenBoolCheckboxes = this.boolFilterGetNonHidden(boolFilter);
          nonHiddenBoolCheckboxes.forEach((checkbox) => {
            url = this.addAndIfNotFirstFilter(url, isFirstFilter);
            url = this.addToURLNotHidden(url, true, checkbox.name, boolFilter.columnName);
            isFirstFilter = false;
          });
        }
      });
    }

    durationFilters.forEach((durationFilter) => {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
      const startTime = this.getTimeForDurationURL(durationFilter.startTime);
      const endTime = this.getTimeForDurationURL(durationFilter.endTime);
      url = this.addToURLRangeNotHidden(url, startTime, endTime, 'duration');
      isFirstFilter = false;
    });

    jobIdFilters.forEach((jobIdFilter) => {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
      url = this.addToURLContainFilter(url, jobIdFilter.searchText, 'job_id');
      isFirstFilter = false;
    });

    startTimeFilters.forEach((startTimeFilter) => {
      url = this.addAndIfNotFirstFilter(url, isFirstFilter);
      // time format for api is MM_DD_YY_HH_mm
      const startTime = this.getTimeForStartTimeURL(startTimeFilter.startTime);
      const endTime = this.getTimeForStartTimeURL(startTimeFilter.endTime);
      url = this.addToURLRangeNotHidden(url, startTime, endTime, 'start_time');
      isFirstFilter = false;
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

  static getAllFilters(
    statuses, allUsers, hiddenUsers, numberFilters, containFilters, boolFilters, durationFilters, jobIdFilters,
    startTimeFilters,
  ) {
    let updatedFilters = [];
    if (hiddenUsers.length > 0) {
      const visibleUsers = this.getVisibleFromFilter(allUsers, hiddenUsers);
      updatedFilters = this.getFilters(visibleUsers, 'User');
    }

    if (numberFilters.length > 0) {
      numberFilters.forEach((numberFilter) => {
        const newRangeFilter = this.getRangeFilter(numberFilter.columnName, numberFilter.min, numberFilter.max);
        updatedFilters.push(newRangeFilter);
      });
    }

    if (containFilters.length > 0) {
      containFilters.forEach((containFilter) => {
        const newContainFilter = this.getContainFilter(containFilter.columnName, containFilter.searchText);
        updatedFilters.push(newContainFilter);
      });
    }

    if (this.boolFilterArrayHasHidden(boolFilters)) {
      boolFilters.forEach((boolFilter) => {
        if (this.boolFilterHasHidden(boolFilter)) {
          const nonHiddenBoolCheckboxes = this.boolFilterGetNonHidden(boolFilter);
          nonHiddenBoolCheckboxes.forEach((checkbox) => {
            const newboolFilter = this.getFilterObject(boolFilter.columnName, checkbox.name);
            updatedFilters.push(newboolFilter);
          });
        }
      });
    }

    if (durationFilters.length > 0) {
      durationFilters.forEach((durationFilter) => {
        const startTime = this.getTimeForDurationBubble(durationFilter.startTime);
        const endTime = this.getTimeForDurationBubble(durationFilter.endTime);
        const newRangeFilter = this.getRangeFilter('Duration', startTime, endTime);
        updatedFilters.push(newRangeFilter);
      });
    }

    if (jobIdFilters.length > 0) {
      jobIdFilters.forEach((jobIdFilter) => {
        const newJobIdFilter = this.getContainFilter(jobIdFilter.columnName, jobIdFilter.searchText);
        updatedFilters.push(newJobIdFilter);
      });
    }

    if (startTimeFilters.length > 0) {
      startTimeFilters.forEach((startTimeFilter) => {
        const startTime = this.getTimeForStartTimeBubble(startTimeFilter.startTime);
        const endTime = this.getTimeForStartTimeBubble(startTimeFilter.endTime);
        const newRangeFilter = this.getRangeFilter('Start Time', startTime, endTime);
        updatedFilters.push(newRangeFilter);
      });
    }

    return this.getStatusFilters(updatedFilters, statuses);
  }

  static getFilters(filters, colName) {
    const updatedFilters = [];
    filters.forEach((value) => {
      const newFilter = this.getFilterObject(colName, value);
      updatedFilters.push(newFilter);
    });
    return updatedFilters;
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
      noStatusFilters = this.getUpdatedStatusesFromOldStatuses(filters, status, noStatusFilters, newStatuses);
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

  static addStatusToURLNotHidden(url, isFirstStatus, status) {
    let newUrl = url;
    if (status.hidden === false) {
      newUrl = this.addToURL(url, isFirstStatus, status.name, 'status');
    }
    return newUrl;
  }

  static addToURL(url, isFirst, value, colName) {
    let newURL = url;
    if (isFirst) {
      newURL += colName.concat('=').concat(value);
    } else {
      newURL += ','.concat(value);
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
          return true;
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
    let newNoStatusFilters = noStatusFilters;
    filters.forEach((filter) => {
      if (this.doesFilterExist(filter, statusInFilter)) {
        isHidden = false;
        newNoStatusFilters = false;
      }
    });
    newStatuses.push({ name: status.name, hidden: isHidden });
    return newNoStatusFilters;
  }

  static getAllJobUsers(jobs) {
    const users = [];
    jobs.forEach((job) => {
      const userExists = users.some((user) => {
        return (user.name === job.user);
      });
      if (!userExists) {
        users.push({ name: job.user, hidden: false });
      }
    });
    return users;
  }

  static addToURLNotHidden(url, isFirst, value, columnName) {
    let newUrl = url;
    newUrl = this.addToURL(url, isFirst, value, columnName);
    return newUrl;
  }

  static addAndIfNotFirstFilter(url, isFirst) {
    let newUrl = url;
    if (!isFirst) {
      newUrl += '&';
    }
    return newUrl;
  }

  static getVisibleFromFilter(allValues, hiddenValues) {
    const visibleValues = allValues.filter(
      (value) => {
        if (!hiddenValues.includes(value)) {
          return true;
        }
      },
    );
    return visibleValues;
  }

  static updateHiddenParams(allParams, newHiddenParam, allHiddenParams) {
    // Check is this param related to this hidden set
    if (!allParams.includes(newHiddenParam)) {
      return allHiddenParams;
    }
    if (this.willHideAllParams(allParams, allHiddenParams)) {
      return [];
    }
    const newHiddenParams = CommonActions.deepCopyArray(allHiddenParams);
    newHiddenParams.push(newHiddenParam);
    return newHiddenParams;
  }

  static willHideAllParams(allParams, allHiddenParams) {
    return allHiddenParams.length + 1 === allParams.length;
  }

  static addToURLRangeNotHidden(url, startValue, endValue, columnName) {
    let newUrl = url;
    const addToURLValue = columnName.concat('_starts=')
      .concat(startValue)
      .concat('&')
      .concat(columnName)
      .concat('_ends=')
      .concat(endValue);
    newUrl += addToURLValue;
    return newUrl;
  }

  static getRangeFilter(colName, startRange, endRange) {
    const rangeValue = startRange.toString().concat(' - ').concat(endRange.toString());
    return this.getFilterObject(colName, rangeValue);
  }

  static getExistingValuesForFilter(allFilters, colName) {
    const existingFilters = allFilters.filter((filter) => {
      if (filter.columnName === colName) {
        return true;
      }
    });

    if (existingFilters.length > 0) {
      return existingFilters[0];
    }
    return null;
  }

  static removeFilterByName(rangeFilters, removeFilter) {
    return rangeFilters.filter((filter) => {
      if (filter.columnName !== removeFilter.column) {
        return true;
      }
    });
  }

  static addToURLContainFilter(url, value, columnName) {
    let newUrl = url;
    const containColName = columnName.concat('_contains');
    newUrl = this.addToURL(url, true, value, containColName);
    return newUrl;
  }

  static getContainFilter(colName, value) {
    const containValue = '"'.concat(value).concat('"');
    return this.getFilterObject(colName, containValue);
  }

  static boolFilterHasHidden(boolFilter) {
    const hasHidden = boolFilter.boolCheckboxes.filter((checkbox) => {
      return checkbox.hidden === true;
    });
    return hasHidden.length > 0;
  }

  static boolFilterArrayHasHidden(boolFilters) {
    let hasHidden = false;
    boolFilters.forEach((filter) => {
      hasHidden = hasHidden || this.boolFilterHasHidden(filter);
    });
    return hasHidden;
  }

  static boolFilterGetNonHidden(boolFilter) {
    const filtersWithoutHidden = boolFilter.boolCheckboxes.filter((checkbox) => {
      return checkbox.hidden === false;
    });
    return filtersWithoutHidden;
  }

  static boolFilterGetHidden(boolFilter) {
    const filtersOnlyHidden = boolFilter.filter((checkbox) => {
      return checkbox.hidden !== false;
    });

    return CommonActions.getFlatArray(filtersOnlyHidden);
  }

  static getTimeForDurationURL(time) {
    return `${time.days}_${time.hours}_${time.minutes}_${time.seconds}`;
  }

  static getTimeForDurationBubble(time) {
    return `${time.days}d${time.hours}h${time.minutes}m${time.seconds}s`;
  }

  static areNoFilters(statusFilter, userFilter, numberFilters, containFilters, boolFilters, durationFilters,
    jobIdFilters, startTimeFilters) {
    const arrayFilters = [userFilter, numberFilters, containFilters, durationFilters, jobIdFilters, startTimeFilters];
    const mappedFilters = arrayFilters.filter((filter) => {
      return filter.length !== 0;
    });
    return !this.areStatusesHidden(statusFilter)
    && !this.boolFilterArrayHasHidden(boolFilters)
    && mappedFilters.length === 0;
  }

  static getTimeForStartTimeURL(time) {
    // time format for api is MM_DD_YY_HH_mm
    const date = new Date(time);
    return `${this.prependZero(date.getMonth() + 1)}_${this.prependZero(date.getDate())}_${date.getFullYear()}`
    + `_${this.prependZero(date.getHours())}_${this.prependZero(date.getMinutes())}`;
  }

  static prependZero(time) {
    return ('0'.concat(time)).slice(-2);
  }

  static getTimeForStartTimeBubble(time) {
    const date = new Date(time);
    const year = date.getFullYear().toString().substr(-2);

    return `${this.prependZero(date.getMonth() + 1)}/${this.prependZero(date.getDate())}/`
    + `${year} ${this.prependZero(date.getHours())}:${this.prependZero(date.getMinutes())}`;
  }

  static isColumnFiltered(filteredArray, columnName) {
    const filteredArrayMapped = filteredArray.map((filter) => {
      return filter.column;
    });
    return filteredArrayMapped.includes(columnName);
  }

  static redirect(url) {
    return BaseActions.redirectRoute(url);
  }

  static deleteAllJobs(jobIds, callback) {
    const deletedJobRequests = jobIds.map(
      (jobId) => {
        const uri = `projects/dummy_project_name/job_listing/${jobId}`;
        return BaseActions.deleteBetaFromAPI(uri);
      },
    );
    return Promise.all(deletedJobRequests).then(callback);
  }
}

export default JobListActions;
