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
    this.onChangeStartDateDay = this.onChangeStartDateDay.bind(this);
    this.onChangeStartDateHour = this.onChangeStartDateHour.bind(this);
    this.onChangeStartDateMinute = this.onChangeStartDateMinute.bind(this);
    this.onChangeStartDateSecond = this.onChangeStartDateSecond.bind(this);
    this.onChangeEndDateDay = this.onChangeEndDateDay.bind(this);
    this.onChangeEndDateHour = this.onChangeEndDateHour.bind(this);
    this.onChangeEndDateMinute = this.onChangeEndDateMinute.bind(this);
    this.onChangeEndDateSecond = this.onChangeEndDateSecond.bind(this);
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

  onChangeStartDateDay(e) {
    const { startTime } = this.state;
    let newStartTime = startTime;
    newStartTime.days = e.target.value;
    this.setState({ startTime: newStartTime });
  }

  onChangeStartDateHour(e) {
    const { startTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 23) {
      let newStartTime = startTime;
      newStartTime.hours = e.target.value;
      this.setState({ startTime: newStartTime });
    }
  }

  onChangeStartDateMinute(e) {
    const { startTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 59) {
      let newStartTime = startTime;
      newStartTime.minutes = e.target.value;
      this.setState({ startTime: newStartTime });
    }
  }

  onChangeStartDateSecond(e) {
    const { startTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 59) {
      let newStartTime = startTime;
      newStartTime.seconds = e.target.value;
      this.setState({ startTime: newStartTime });
    }
  }

  onChangeEndDateDay(e) {
    const { endTime } = this.state;
    let newEndTime = endTime;
    newEndTime.days = e.target.value;
    this.setState({ endTime: newEndTime });
  }

  onChangeEndDateHour(e) {
    const { endTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 23) {
      let newEndTime = endTime;
      newEndTime.hours = e.target.value;
      this.setState({ endTime: newEndTime });
    }
  }

  onChangeEndDateMinute(e) {
    const { endTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 59) {
      let newEndTime = endTime;
      newEndTime.minutes = e.target.value;
      this.setState({ endTime: newEndTime });
    }
  }

  onChangeEndDateSecond(e) {
    const { endTime } = this.state;
    if (e.target.value >= 0 && e.target.value <= 59) {
      let newEndTime = endTime;
      newEndTime.seconds = e.target.value;
      this.setState({ endTime: newEndTime });
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
              onChange={(e) => { this.onChangeStartDateDay(e); }}
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
              onChange={(e) => { this.onChangeStartDateHour(e); }}
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
              onChange={(e) => { this.onChangeStartDateMinute(e); }}
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
              onChange={(e) => { this.onChangeStartDateSecond(e); }}
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
              onChange={(e) => { this.onChangeEndDateDay(e); }}
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
              onChange={(e) => { this.onChangeEndDateHour(e); }}
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
              onChange={(e) => { this.onChangeEndDateMinute(e); }}
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
              onChange={(e) => { this.onChangeEndDateSecond(e); }}
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
