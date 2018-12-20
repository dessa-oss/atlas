import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Checkbox from '../Checkbox';
import CommonActions from '../../../actions/CommonActions';

class NumberFilter extends Component {
  constructor(props) {
    super(props);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.onChangeMin = this.onChangeMin.bind(this);
    this.onChangeMax = this.onChangeMax.bind(this);
    this.onChangeCheckbox = this.onChangeCheckbox.bind(this);
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      minValue: this.props.minValue,
      maxValue: this.props.maxValue,
      hideNotAvailable: false,
      columnName: this.props.columnName,
      showAllFilters: false,
      metricClass: this.props.metricClass,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        maxValue: nextProps.maxValue,
        minValue: nextProps.minValue,
        columnName: nextProps.columnName,
        metricClass: nextProps.metricClass,
      },
    );
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, columnName, minValue, maxValue, hideNotAvailable,
    } = this.state;
    if (!this.isDisabled()) {
      changeHiddenParams(minValue, maxValue, hideNotAvailable, columnName);
      toggleShowingFilter();
    }
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    toggleShowingFilter();
  }

  onClearFilters() {
    this.setState({ minValue: 0, maxValue: 0, showAllFilters: true });
  }

  onChangeMin(e) {
    this.setState({ minValue: e.target.value });
  }

  onChangeMax(e) {
    this.setState({ maxValue: e.target.value });
  }

  onChangeCheckbox() {
    const { hideNotAvailable } = this.state;
    this.setState({ hideNotAvailable: !hideNotAvailable, showAllFilters: false });
  }

  isDisabled() {
    const { minValue, maxValue } = this.state;
    return minValue > maxValue || minValue === '' || maxValue === '';
  }

  render() {
    const {
      minValue, maxValue, hideNotAvailable, showAllFilters, metricClass,
    } = this.state;

    const divClass = 'filter-container column-filter-container elevation-1 number-filter-container '
      .concat(metricClass);

    const applyClass = CommonActions.getApplyClass(this.isDisabled);

    return (
      <div className={divClass}>
        <div className="column-filter-header">
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <div className="number-input-container">
          <div>
            <label htmlFor="filter-input-sec">Min</label>
            <input
              type="number"
              id="filter-input-sec"
              placeholder="Min"
              value={minValue}
              onChange={(e) => { this.onChangeMin(e); }}
            />
          </div>
          <div> - </div>
          <div>
            <label htmlFor="filter-input-sec">Max</label>
            <input
              type="number"
              id="filter-input-sec"
              placeholder="Max"
              value={maxValue}
              onChange={(e) => { this.onChangeMax(e); }}
            />
          </div>
        </div>

        {/* <Checkbox
          name="Show 'not available' values"
          hidden={hideNotAvailable}
          changeHiddenParams={this.onChangeCheckbox}
          showAllFilters={showAllFilters}
        /> */}

        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className={applyClass}>Apply</button>
        </div>
      </div>
    );
  }
}

NumberFilter.propTypes = {
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  minValue: PropTypes.number,
  maxValue: PropTypes.number,
  hideNotAvailable: PropTypes.bool,
  columnName: PropTypes.string,
  showAllFilters: PropTypes.bool,
  metricClass: PropTypes.string,
};

NumberFilter.defaultProps = {
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  minValue: 0,
  maxValue: 0,
  hideNotAvailable: false,
  columnName: '',
  showAllFilters: false,
  metricClass: 'not-metric',
};

export default NumberFilter;
