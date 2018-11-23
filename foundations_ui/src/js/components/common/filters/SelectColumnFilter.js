import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

class SelectColumnFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.updateSearchText = this.updateSearchText.bind(this);
    this.submitSearchText = this.submitSearchText.bind(this);
    this.unsetClearFilters = this.unsetClearFilters.bind(this);
    this.state = {
      columns: this.props.columns,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: this.props.hiddenInputParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      updateSearchText: this.props.updateSearchText,
      searchText: '',
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
    const { updateSearchText } = this.state;
    const emptyArray = [];
    this.setState({ changedParams: emptyArray, showAllFilters: true });
    updateSearchText('');
    this.input.value = '';
  }

  unsetClearFilters() {
    this.setState({ showAllFilters: false });
  }

  changeLocalParams(colName) {
    const { changedParams } = this.state;
    const copyArray = CommonActions.getChangedCheckboxes(changedParams, colName);
    this.setState({ changedParams: copyArray });
  }

  updateSearchText(e) {
    this.setState({ searchText: e.target.value });
  }

  submitSearchText() {
    const { searchText, updateSearchText } = this.state;
    updateSearchText(searchText);
  }

  render() {
    const { columns, showAllFilters } = this.state;
    const checkboxes = CommonActions.getCheckboxes(
      columns, this.changeLocalParams, showAllFilters, this.unsetClearFilters,
    );

    return (
      <div className="filter-container column-filter-container elevation-1">
        <div className="column-filter-header">
          <input ref={(e) => { this.input = e; }} type="text" onChange={this.updateSearchText} />
          <button
            className="button-icon"
            type="button"
            onClick={this.submitSearchText}
            onKeyPress={this.submitSearchText}
          >
            <div className="magnifying-glass" />
          </button>
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
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

SelectColumnFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  updateSearchText: PropTypes.func,
  showAllFilters: PropTypes.bool,
};

SelectColumnFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  updateSearchText: () => {},
  showAllFilters: false,
};

export default SelectColumnFilter;
