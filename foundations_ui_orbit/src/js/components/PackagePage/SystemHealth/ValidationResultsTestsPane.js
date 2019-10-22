import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsTestsPane extends Component {
  render() {
    const { validationTestResult } = this.props;
    const emptyState = (
      <div className="validation-results-tests-pane-empty-state">
        <div className="i--icon-clipboard" />
        <div className="validation-results-tests-pane-empty-state-text">
          Click on a test to see its details.
        </div>
      </div>
    );

    let mainContent = emptyState;
    if (validationTestResult) {
      mainContent = Object.keys(validationTestResult)[0];
    }

    return (
      <div className="validation-results-tests-pane">
        {mainContent}
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
