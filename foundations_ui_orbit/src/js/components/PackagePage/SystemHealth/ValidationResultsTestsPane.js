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
      console.log(validationTestResult);
      mainContent = (
        <div className="validation-results-test-pane-table-container">
          <table className="validation-results-test-pane-table">
            <tbody>
              <tr className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
                <th>Attribute Name</th>
                <th>Data Type</th>
                <th>Issue Type</th>
                <th>Validation Outcome</th>
              </tr>
            </tbody>
          </table>
        </div>
      );
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
