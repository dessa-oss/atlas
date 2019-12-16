import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ValidationResultsActions from '../../../actions/ValidationResultsActions';

class ValidationResultsTestsList extends Component {
  render() {
    const { validationResult, onSelectRow, selectedRow } = this.props;
    const rows = ValidationResultsActions.getTestRows(validationResult, onSelectRow);

    const rowsWithProps = rows.map(row => React.cloneElement(
      row,
      { selectedRow: selectedRow },
    ));

    return (
      <div className="validation-results-tests-list">
        {rowsWithProps}
      </div>
    );
  }
}

ValidationResultsTestsList.propTypes = {
  validationResult: PropTypes.object,
  onSelectRow: PropTypes.func,
  selectedRow: PropTypes.string,
};

ValidationResultsTestsList.defaultProps = {
  validationResult: {},
  onSelectRow: () => {},
  selectedRow: '',
};

export default ValidationResultsTestsList;
