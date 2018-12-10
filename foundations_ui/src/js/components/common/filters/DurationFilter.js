import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

const isStatusCheckbox = true;

class DurationFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.unsetClearFilters = this.unsetClearFilters.bind(this);
    this.state = {
      columns: this.props.columns,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: this.props.hiddenInputParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      showAllFilters: false,
    };
  }


  componentWillReceiveProps(nextProps) {
    this.setState({ columns: nextProps.columns });
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

  unsetClearFilters() {
    this.setState({ showAllFilters: false });
  }

  changeLocalParams(colName) {
    const { changedParams } = this.state;
    const copyArray = CommonActions.getChangedCheckboxes(changedParams, colName);
    this.setState({ changedParams: copyArray });
  }

  render() {
    const { columns, showAllFilters } = this.state;

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
            <input id="filter-input-days" placeholder="days" />
            <label htmlFor="filter-input-days">days</label>
          </div>
          <div>
            <input id="filter-input-hours" placeholder="hrs" />
            <label htmlFor="filter-input-hours">hrs</label>
          </div>
          <div>
            <input id="filter-input-min" placeholder="min" />
            <label htmlFor="filter-input-min">min</label>
          </div>
          <div>
            <input id="filter-input-sec" placeholder="sec" />
            <label htmlFor="filter-input-sec">sec</label>
          </div>
        </div>
        <p>and</p>
        <div className="guided-input-container">
          <div>
            <input id="filter-input-days" placeholder="days" />
            <label htmlFor="filter-input-days">days</label>
          </div>
          <div>
            <input id="filter-input-hours" placeholder="hrs" />
            <label htmlFor="filter-input-hours">hrs</label>
          </div>
          <div>
            <input id="filter-input-min" placeholder="min" />
            <label htmlFor="filter-input-min">min</label>
          </div>
          <div>
            <input id="filter-input-sec" placeholder="sec" />
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
};

DurationFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  showAllFilters: false,
};

export default DurationFilter;
