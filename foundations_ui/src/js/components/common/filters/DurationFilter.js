import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

const defaultTime = {
  days: '0', hours: '0', minutes: '0', seconds: '0',
};

class DurationFilter extends Component {
  constructor(props) {
    super(props);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onChangeTime = this.onChangeTime.bind(this);
    this.updateInterval = this.updateInterval.bind(this);
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      startTime: this.props.startTime,
      endTime: this.props.endTime,
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
    };
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, startTime, endTime,
    } = this.state;
    if (!this.isDisabled()) {
      changeHiddenParams(startTime, endTime);
      toggleShowingFilter();
    }
  }

  async onCancel() {
    const { toggleShowingFilter } = this.state;
    await this.onClearFilters();
    toggleShowingFilter();
  }

  async onClearFilters() {
    await this.setState({
      startTime: CommonActions.deepCopyArray(defaultTime), endTime: CommonActions.deepCopyArray(defaultTime),
    });
  }

  onChangeTime(e, isStart, minValue, maxValue, interval) {
    if (minValue !== null && maxValue !== null) {
      if (e.target.value >= minValue && e.target.value <= maxValue) {
        this.updateInterval(e, isStart, interval);
      }
    } else {
      this.updateInterval(e, isStart, interval);
    }
  }

  async updateInterval(e, isStart, interval) {
    const { startTime, endTime } = this.state;
    let newTime = CommonActions.deepCopyArray(endTime);
    if (isStart) {
      newTime = CommonActions.deepCopyArray(startTime);
    }
    if (interval === 'days') {
      newTime.days = e.target.value;
    } else if (interval === 'hours') {
      newTime.hours = e.target.value;
    } else if (interval === 'minutes') {
      newTime.minutes = e.target.value;
    } else if (interval === 'seconds') {
      newTime.seconds = e.target.value;
    }
    if (isStart) {
      await this.setState({ startTime: newTime });
    } else {
      await this.setState({ endTime: newTime });
    }
  }

  isDisabled() {
    const { startTime, endTime } = this.state;
    const startNumber = parseInt(`${startTime.days}${startTime.hours}${startTime.minutes}${startTime.seconds}`, 10);
    const endNumber = parseInt(`${endTime.days}${endTime.hours}${endTime.minutes}${endTime.seconds}`, 10);
    return startTime.days === '' || startTime.hours === '' || startTime.minutes === '' || startTime.seconds === ''
      || endTime.days === '' || endTime.hours === '' || endTime.minutes === '' || endTime.seconds === ''
      || startNumber < 0 || endNumber < 0 || startNumber > endNumber;
  }

  render() {
    const { startTime, endTime } = this.state;

    const applyClass = CommonActions.getApplyClass(this.isDisabled);

    return (
      <div className="filter-container column-filter-container elevation-1 duration-filter-container">
        <div className="column-filter-header">
          <p>between</p>
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <div className="guided-input-container">
          <div>
            <input
              type="number"
              min="0"
              id="filter-input-days"
              placeholder="days"
              value={startTime.days}
              onChange={(e) => { this.onChangeTime(e, true, null, null, 'days'); }}
            />
            <label htmlFor="filter-input-days">days</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="23"
              id="filter-input-hours"
              placeholder="hrs"
              value={startTime.hours}
              onChange={(e) => { this.onChangeTime(e, true, 0, 23, 'hours'); }}
            />
            <label htmlFor="filter-input-hours">hrs</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="59"
              id="filter-input-min"
              placeholder="min"
              value={startTime.minutes}
              onChange={(e) => { this.onChangeTime(e, true, 0, 59, 'minutes'); }}
            />
            <label htmlFor="filter-input-min">min</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="59"
              id="filter-input-sec"
              placeholder="sec"
              value={startTime.seconds}
              onChange={(e) => { this.onChangeTime(e, true, 0, 59, 'seconds'); }}
            />
            <label htmlFor="filter-input-sec">sec</label>
          </div>
        </div>
        <p>and</p>
        <div className="guided-input-container">
          <div>
            <input
              type="number"
              min="0"
              id="filter-input-days"
              placeholder="days"
              value={endTime.days}
              onChange={(e) => { this.onChangeTime(e, false, null, null, 'days'); }}
            />
            <label htmlFor="filter-input-days">days</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="23"
              id="filter-input-hours"
              placeholder="hrs"
              value={endTime.hours}
              onChange={(e) => { this.onChangeTime(e, false, 0, 23, 'hours'); }}
            />
            <label htmlFor="filter-input-hours">hrs</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="59"
              id="filter-input-min"
              placeholder="min"
              value={endTime.minutes}
              onChange={(e) => { this.onChangeTime(e, false, 0, 59, 'minutes'); }}
            />
            <label htmlFor="filter-input-min">min</label>
          </div>
          <div>
            <input
              type="number"
              min="0"
              max="59"
              id="filter-input-sec"
              placeholder="sec"
              value={endTime.seconds}
              onChange={(e) => { this.onChangeTime(e, false, 0, 59, 'seconds'); }}
            />
            <label htmlFor="filter-input-sec">sec</label>
          </div>
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className={applyClass}>Apply</button>
        </div>
      </div>
    );
  }
}

DurationFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  startTime: PropTypes.object,
  endTime: PropTypes.object,
};

DurationFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  startTime: {
    days: '0', hours: '0', minutes: '0', seconds: '0',
  },
  endTime: {
    days: '0', hours: '0', minutes: '0', seconds: '0',
  },
};

export default DurationFilter;
