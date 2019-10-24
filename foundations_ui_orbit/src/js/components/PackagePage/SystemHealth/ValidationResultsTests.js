import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsTestsList from "./ValidationResultsTestsList";
import ValidationResultsTestsPane from "./ValidationResultsTestsPane";

class ValidationResultsTests extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedRow: null
    };

    this.selectRow = this.selectRow.bind(this);
  }

  selectRow(rowIndex) {
    this.setState({ selectedRow: rowIndex });
  }

  render() {
    const { selectedRow } = this.state;
    const { validationResult } = this.props;

    let selectedTest = null;
    if (selectedRow) {
      selectedTest = {};
      selectedTest[selectedRow] = validationResult[selectedRow];
    }

    return (
      <div className="validation-results-tests">
        <ValidationResultsTestsList
          validationResult={validationResult}
          onSelectRow={this.selectRow}
          selectedRow={selectedRow}
        />
        <ValidationResultsTestsPane validationTestResult={selectedTest} />
      </div>
    );
  }
}

ValidationResultsTests.propTypes = {
  validationResult: PropTypes.object
};

ValidationResultsTests.defaultProps = {
  validationResult: {}
};

export default ValidationResultsTests;
