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
    this.onPickerClose = this.onPickerClose.bind(this);
    this.onPickerOpen = this.onPickerOpen.bind(this);
    this.openClosePicker = this.openClosePicker.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      startDate: this.props.startDate,
      endDate: this.props.endDate,
      isStartPickerOpen: false,
      isEndPickerOpen: false,
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

  async onPickerClose(isStartPicker) {
    if (isStartPicker) {
      await this.setState({ isStartPickerOpen: false });
    } else {
      await this.setState({ isEndPickerOpen: false });
    }
  }

  async onPickerOpen(isStartPicker) {
    if (isStartPicker) {
      await this.setState({ isStartPickerOpen: true });
    } else {
      await this.setState({ isEndPickerOpen: true });
    }
  }

  async openClosePicker(isStartPicker, isOpening) {
    let picker = this.endPicker;
    if (isStartPicker) {
      picker = this.startPicker;
    }

    if (isOpening) {
      await picker.flatpickr.open();
    }
  }

  render() {
    const {
      startDate, endDate, isStartPickerOpen, isEndPickerOpen,
    } = this.state;

    let startCalButton = (
      <div
        className="i--icon-cal-clock"
        role="presentation"
        onClick={() => { this.onPickerOpen(true); this.openClosePicker(true, true); }}
      />
    );
    if (isStartPickerOpen) {
      startCalButton = (
        <div
          className="i--icon-cal-clock"
          style={{ 'background-color': 'red' }}
          role="presentation"
          onClick={() => { this.onPickerClose(true); this.openClosePicker(true, false); }}
        />
      );
    }

    let endCalButton = (
      <div
        className="i--icon-cal-clock"
        role="presentation"
        onClick={() => { this.onPickerOpen(false); this.openClosePicker(false, true); }}
      />
    );
    if (isEndPickerOpen) {
      endCalButton = (
        <div
          className="i--icon-cal-clock"
          role="presentation"
          onClick={() => { this.onPickerClose(false); this.openClosePicker(false, false); }}
        />
      );
    }

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
          {startCalButton}
          <Flatpickr
            // options={{ clickOpens: false }}
            data-enable-time
            id="start-flatpicker"
            ref={(startPicker) => { this.startPicker = startPicker; }}
            value={startDate}
            onChange={(e) => { this.onChangeDateTime(e, true); }}
            onClose={() => { this.onPickerClose(true); }}
            onOpen={() => { }}
            onClick={() => {}}
          />
        </div>
        <p>and</p>
        <div className="date-time-picker">
          {endCalButton}
          <Flatpickr
            data-enable-time
            value={endDate}
            id="end-flatpicker"
            ref={(endPicker) => { this.endPicker = endPicker; }}
            onChange={(e) => { this.onChangeDateTime(e, false); }}
            onClose={() => { this.onPickerClose(false); }}
            onOpen={() => { this.onPickerOpen(false); }}
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
  isStartPickerOpen: PropTypes.bool,
  isEndPickerOpen: PropTypes.bool,
};

DateTimeFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  startDate: null,
  endDate: null,
  isStartPickerOpen: false,
  isEndPickerOpen: false,
};

export default DateTimeFilter;
