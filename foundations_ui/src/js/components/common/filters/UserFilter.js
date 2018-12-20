import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';
import CheckboxFilter from './CheckboxFilter';

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
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      columns: this.props.columns,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: this.props.hiddenInputParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      searchUserFilter: this.props.searchUserFilter,
      searchText: '',
      showAllFilters: false,
    };
  }


  componentWillReceiveProps(nextProps) {
    const { unsetClearFilters } = this.state;
    if (unsetClearFilters) {
      this.setState({ columns: nextProps.columns, changedParams: nextProps.hiddenInputParams });
    }
  }

  onApply() {
    const {
      changeHiddenParams, changedParams, toggleShowingFilter, searchUserFilter,
    } = this.state;
    if (!this.isDisabled()) {
      this.setState({ searchText: '' });
      changeHiddenParams(changedParams);
      searchUserFilter('');
      toggleShowingFilter();
    }
  }

  onCancel() {
    const { toggleShowingFilter, searchUserFilter } = this.state;
    this.setState({ changedParams: [], searchText: '' });
    searchUserFilter('');
    toggleShowingFilter();
  }

  onClearFilters() {
    const { searchUserFilter } = this.state;
    const emptyArray = [];
    this.setState({ changedParams: emptyArray, showAllFilters: true });
    searchUserFilter('');
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
    const { searchText, searchUserFilter } = this.state;
    searchUserFilter(searchText);
  }

  isDisabled() {
    const { columns, changedParams } = this.state;
    return changedParams.length >= columns.length;
  }

  render() {
    const { columns, showAllFilters, changedParams } = this.state;
    const checkboxes = CommonActions.getCheckboxes(
      columns, this.changeLocalParams, showAllFilters, this.unsetClearFilters,
    );

    const input = <input ref={(inputRef) => { this.input = inputRef; }} type="text" onChange={this.updateSearchText} />;

    const applyClass = CommonActions.getApplyClass(this.isDisabled);

    return (
      <CheckboxFilter
        checkboxes={checkboxes}
        onCancel={this.onCancel}
        onApply={this.onApply}
        submitSearchText={this.submitSearchText}
        onClearFilters={this.onClearFilters}
        input={input}
        addedClass="user-filter-container"
        applyClass={applyClass}
      />);
  }
}

SelectColumnFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
  hiddenInputParams: PropTypes.array,
  searchUserFilter: PropTypes.func,
  showAllFilters: PropTypes.bool,
};

SelectColumnFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
  hiddenInputParams: [],
  searchUserFilter: () => {},
  showAllFilters: false,
};

export default SelectColumnFilter;
