import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";
import ValidationResultsOverview from "./ValidationResultsOverview";
import ValidationResultsTests from "./ValidationResultsTests";

class ValidationResultsDetails extends Component {
  render() {
    const { selectedValidationResult } = this.props;
    let test = "test";
    if (selectedValidationResult) {
      test = selectedValidationResult.time
      + selectedValidationResult.monitorName
      + selectedValidationResult.contractName;
    }

    return (
      <div className="validation-results-details">
        <ValidationResultsOverview />
        <ValidationResultsTests />
      </div>
    );
  }
}

ValidationResultsDetails.propTypes = {
  selectedValidationResult: PropTypes.object
};

ValidationResultsDetails.defaultProps = {
  selectedValidationResult: {}
};

export default ValidationResultsDetails;
