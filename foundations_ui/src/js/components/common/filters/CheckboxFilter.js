import React, { Component } from 'react';
import PropTypes from 'prop-types';

class CheckboxFilter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      checkboxes: this.props.checkboxes,
      onCancel: this.props.onCancel,
      onApply: this.props.onApply,
      submitSearchText: this.props.submitSearchText,
      onClearFilters: this.props.onClearFilters,
      input: this.props.input,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ checkboxes: nextProps.checkboxes });
  }

  render() {
    const {
      checkboxes, onCancel, onApply, submitSearchText, onClearFilters, input,
    } = this.state;
    return (
      <div className="filter-container column-filter-container elevation-1">
        <div className="column-filter-header">
          {input}
          <button
            className="button-icon"
            type="button"
            onClick={submitSearchText}
            onKeyPress={submitSearchText}
          >
            <div className="magnifying-glass" />
          </button>
          <button
            type="button"
            onClick={onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <div className="column-filter-list">
          {checkboxes}
        </div>
        <div className="column-filter-buttons">
          <button type="button" onClick={onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

CheckboxFilter.propTypes = {
  checkboxes: PropTypes.array,
  onCancel: PropTypes.func,
  onApply: PropTypes.func,
  submitSearchText: PropTypes.func,
  onClearFilters: PropTypes.func,
  input: PropTypes.object,
};

CheckboxFilter.defaultProps = {
  checkboxes: [],
  onCancel: () => {},
  onApply: () => {},
  submitSearchText: () => {},
  onClearFilters: () => {},
  input: null,
};

export default CheckboxFilter;
