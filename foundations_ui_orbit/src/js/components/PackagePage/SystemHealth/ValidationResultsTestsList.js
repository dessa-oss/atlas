import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsTestsList extends Component {
  render() {
    const { validationResult, onSelectRow } = this.props;
    const rows = ValidationResultsActions.getTestRows(validationResult, onSelectRow);

    return (
      <div className="validation-results-tests-list">
        {rows}
      </div>
    );
  }
}

ValidationResultsTestsList.propTypes = {
  validationResult: PropTypes.object,
  onSelectRow: PropTypes.func
};

ValidationResultsTestsList.defaultProps = {
  validationResult: {},
  onSelectRow: () => {}
};

export default ValidationResultsTestsList;
