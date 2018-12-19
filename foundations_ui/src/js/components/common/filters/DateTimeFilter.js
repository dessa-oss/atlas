import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Flatpickr from 'react-flatpickr';

class DateTimeFilter extends Component {
  constructor(props) {
    super(props);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onChangeDateTime = this.onChangeDateTime.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      startDate: this.props.startDate,
      endDate: this.props.endDate,
    };
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, startDate, endDate,
    } = this.state;
    changeHiddenParams(startDate, endDate);
    toggleShowingFilter();
  }

  async onCancel() {
    const { toggleShowingFilter } = this.state;
    await this.onClearFilters();
    toggleShowingFilter();
  }

  async onClearFilters() {
    await this.setState({
      startDate: null,
      endDate: null,
    });
  }

  async onChangeDateTime(e, isStartTime) {
    if (isStartTime) {
      await this.setState({ startDate: new Date(e[0]) });
    } else {
      await this.setState({ endDate: new Date(e[0]) });
    }
  }

  render() {
    const { startDate, endDate } = this.state;

    return (
      <div className="filter-container column-filter-container elevation-1 datetime-filter-container">
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
        <div className="date-time-picker">
          <Flatpickr
            data-enable-time
            value={startDate}
            onChange={(e) => { this.onChangeDateTime(e, true); }}
          />
        </div>
        <p>and</p>
        <div className="date-time-picker">
          <Flatpickr
            data-enable-time
            value={endDate}
            onChange={(e) => { this.onChangeDateTime(e, false); }}
          />
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

DateTimeFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  startDate: PropTypes.object,
  endDate: PropTypes.object,
};

DateTimeFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  startDate: null,
  endDate: null,
};

export default DateTimeFilter;
