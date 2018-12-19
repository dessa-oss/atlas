import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

const numCheckboxes = 2;

class BooleanFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.unsetClearFilters = this.unsetClearFilters.bind(this);
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      columnName: this.props.columnName,
      metricClass: this.props.metricClass,
      showAllFilters: false,
      columns: this.props.columns,
      changedParams: this.props.changedParams,
    };
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, changedParams, columnName,
    } = this.state;
    if (!this.isDisabled()) {
      changeHiddenParams(changedParams, columnName);
      toggleShowingFilter();
    }
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

  isDisabled() {
    const { changedParams } = this.state;
    return changedParams.length >= numCheckboxes;
  }

  render() {
    const {
      metricClass, isStatusCheckbox, showAllFilters, columns,
    } = this.state;

    const checkboxes = CommonActions.getCheckboxes(
      columns, this.changeLocalParams, showAllFilters, this.unsetClearFilters, isStatusCheckbox,
    );

    const divClass = 'filter-container column-filter-container elevation-1 boolean-filter-container '
      .concat(metricClass);

    let applyClass = 'b--mat b--affirmative text-upper';
    if (this.isDisabled()) {
      applyClass += ' b--disabled';
    }

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
        <div className="column-filter-list">
          {checkboxes}
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className={applyClass}>Apply</button>
        </div>
      </div>
    );
  }
}

BooleanFilter.propTypes = {
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  columnName: PropTypes.string,
  metricClass: PropTypes.string,
  isStatusCheckbox: PropTypes.bool,
  showAllFilters: PropTypes.bool,
  columns: PropTypes.array,
  changedParams: PropTypes.array,
};

BooleanFilter.defaultProps = {
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  columnName: '',
  metricClass: 'not-metric',
  isStatusCheckbox: false,
  showAllFilters: false,
  columns: [],
  changedParams: [],
};

export default BooleanFilter;
