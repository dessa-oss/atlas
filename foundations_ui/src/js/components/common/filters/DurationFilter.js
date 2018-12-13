import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

class DurationFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.unsetClearFilters = this.unsetClearFilters.bind(this);
    this.onChangeTime = this.onChangeTime.bind(this);
    this.updateInterval = this.updateInterval.bind(this);
    this.state = {
      startTime: this.props.startTime,
      endTime: this.props.endTime,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: this.props.hiddenInputParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
    };
  }

  onApply() {
    const { changeHiddenParams, changedParams, toggleShowingFilter } = this.state;
    changeHiddenParams(changedParams);
    toggleShowingFilter();
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    this.setState({ changedParams: [] });
    toggleShowingFilter();
  }

  onClearFilters() {
    const emptyArray = [];
    this.setState({ changedParams: emptyArray, showAllFilters: true });
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

  updateInterval(e, isStart, interval) {
    const { startTime, endTime } = this.state;
    let newTime = endTime;
    if (isStart) {
      newTime = startTime;
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
      this.setState({ startTime: newTime });
    } else {
      this.setState({ endTime: newTime });
    }
  }

  unsetClearFilters() {
    this.setState({ showAllFilters: false });
  }

  changeLocalParams(colName) {
    const { changedParams } = this.state;
    const copyArray = CommonActions.getChangedCheckboxes(changedParams, colName);
    this.setState({ changedParams: copyArray });
  }

  render() {
    const { startTime, endTime, showAllFilters } = this.state;

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
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

DurationFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  showAllFilters: PropTypes.bool,
  startTime: PropTypes.object,
  endTime: PropTypes.object,
};

DurationFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  showAllFilters: false,
  startTime: {
    days: 0, hours: 0, minutes: 0, seconds: 0,
  },
  endTime: {
    days: 0, hours: 0, minutes: 0, seconds: 0,
  },
};

export default DurationFilter;
