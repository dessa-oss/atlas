import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ValidationResultsActions from '../../../actions/ValidationResultsActions';
import CommonActions from '../../../actions/CommonActions';

class ValidationResultsTestsPane extends Component {
  render() {
    const { validationTestResult } = this.props;
    let mainContent = (
      <div className="validation-results-tests-pane-empty-state">
        <div className="i--icon-clipboard" />
        <div className="validation-results-tests-pane-empty-state-text">
          Click on a test to see its details.
        </div>
      </div>
    );

    if (!CommonActions.isEmptyObject(validationTestResult)) {
      const tableRows = ValidationResultsActions.getTestTableRows(validationTestResult);
      mainContent = (
        <div className="validation-results-test-pane-table-container">
          <table className="validation-results-test-pane-table">
            <tbody>
              {tableRows}
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
  validationTestResult: PropTypes.object,
};

ValidationResultsTestsPane.defaultProps = {
  validationTestResult: {},
};

export default ValidationResultsTestsPane;
