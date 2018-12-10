import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';
import Checkbox from '../Checkbox';

const isStatusCheckbox = true;

class NumberFilter extends Component {
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
    const checkboxes = CommonActions.getCheckboxes(
      columns, this.changeLocalParams, showAllFilters, this.unsetClearFilters, isStatusCheckbox,
    );

    return (
      <div className="filter-container column-filter-container elevation-1 number-filter-container">
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
              onChange={(e) => { this.onChangeStartDateSecond(e); }}
            />
          </div>
          <div> - </div>
          <div>
            <label htmlFor="filter-input-sec">Max</label>
            <input
              type="number"
              id="filter-input-sec"
              placeholder="Max"
              onChange={(e) => { this.onChangeStartDateSecond(e); }}
            />
          </div>
        </div>

        <Checkbox name="Show 'not available' values" hidden={false} />

        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

NumberFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  showAllFilters: PropTypes.bool,
};

NumberFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  showAllFilters: false,
};

export default NumberFilter;
