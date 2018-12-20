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
      addedClass: this.props.addedClass,
      applyClass: this.props.applyClass,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ checkboxes: nextProps.checkboxes, applyClass: nextProps.applyClass });
  }

  render() {
    const {
      checkboxes, onCancel, onApply, submitSearchText, onClearFilters, input, addedClass, applyClass,
    } = this.state;

    const divClass = 'filter-container column-filter-container elevation-1 '.concat(addedClass);

    return (
      <div className={divClass}>
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
          <button type="button" onClick={onApply} className={applyClass}>Apply</button>
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
  addedClass: PropTypes.string,
  applyClass: PropTypes.string,
};

CheckboxFilter.defaultProps = {
  checkboxes: [],
  onCancel: () => {},
  onApply: () => {},
  submitSearchText: () => {},
  onClearFilters: () => {},
  input: null,
  addedClass: '',
  applyClass: 'b--mat b--affirmative text-upper',
};

export default CheckboxFilter;
