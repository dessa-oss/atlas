import React, { Component } from "react";
import PropTypes from "prop-types";

class ValidationResultsTestsListRow extends Component {
  constructor(props) {
    super(props);

    this.onClick = this.onClick.bind(this);
  }

  onClick() {
    const { onSelectRow, objKey } = this.props;
    onSelectRow(objKey);
  }

  render() {
    const { label, validationTestResult } = this.props;

    return (
      <div className="validation-results-tests-list-row" onClick={this.onClick}>
        <div className="validation-results-tests-list-row-header">{label}</div>
        <div className="validation-results-tests-list-row-summary">
          <div className="validation-results-tests-list-row-summary-values">
            {validationTestResult.summary.critical}<br />
            {validationTestResult.summary.healthy}<br />
            {validationTestResult.summary.warning}
          </div>
          <div className="validation-results-tests-list-row-summary-labels">
            Critical<br />
            Healthy<br />
            Warning
          </div>
        </div>
      </div>
    );
  }
}

ValidationResultsTestsListRow.propTypes = {
  label: PropTypes.string,
  objKey: PropTypes.string,
  validationTestResult: PropTypes.object,
  onSelectRow: PropTypes.func
};

ValidationResultsTestsListRow.defaultProps = {
  label: "Invalid test",
  objKey: "",
  validationTestResult: {},
  onSelectRow: () => {}
};

export default ValidationResultsTestsListRow;
