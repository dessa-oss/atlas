import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsTestsPane extends Component {
  render() {
    const { validationTestResult } = this.props;
    let test = "empty state";
    if (validationTestResult) {
      test = Object.keys(validationTestResult)[0];
    }
    return (
      <div className="validation-results-tests-pane">
        {test}
      </div>
    );
  }
}

ValidationResultsTestsPane.propTypes = {
  validationTestResult: PropTypes.object
};

ValidationResultsTestsPane.defaultProps = {
  validationTestResult: {}
};

export default ValidationResultsTestsPane;
