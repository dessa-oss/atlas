import React from 'react';
import { get, post } from './BaseActions';
import ValidationResultsTableRow from '../components/PackagePage/SystemHealth/ValidationResultsTableRow';
import ValidationResultsTestsListRow from '../components/PackagePage/SystemHealth/ValidationResultsTestListRow';
import CommonActions from './CommonActions';
import OverflowTooltip from '../components/common/OverflowTooltip';

const ValidationResultsActions = {
  getValidationResultList: projectName => {
    const url = `projects/${projectName}/validation_report_list`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return [];
      });
  },

  getResultRows: (results, onClickRow) => {
    return results.map(result => {
      const key = result.inference_period + result.model_package + result.data_contract;
      return (
        <ValidationResultsTableRow
          key={key}
          onClick={onClickRow}
          time={result.inference_period}
          monitorName={result.monitor_package}
          contractName={result.data_contract}
          numCritical={result.num_critical_tests}
        />
      );
    });
  },

  getValidationResults: (projectName, inferencePeriod, monitorPackage, dataContract) => {
    const url = `projects/${projectName}/validation_results`;
    const body = {
      inference_period: inferencePeriod,
      monitor_package: monitorPackage,
      data_contract: dataContract,
    };

    return post(url, body)
      .then(results => {
        return results;
      })
      .catch(() => {
        return {};
      });
  },

  createTestRowIfExists: (key, label, allTestResults, allRows, onSelectRow) => {
    if (key in allTestResults) {
      const testResult = allTestResults[key];
      allRows.push(
        <ValidationResultsTestsListRow
          key={key}
          objKey={key}
          label={label}
          validationTestResult={testResult}
          onSelectRow={onSelectRow}
        />,
      );
    }
  },

  getTestRows: (validationResult, onSelectRow) => {
    const allRows = [];
    ValidationResultsActions.createTestRowIfExists('schema', 'Schema Check', validationResult, allRows, onSelectRow);
    ValidationResultsActions.createTestRowIfExists(
      'population_shift', 'Population Shift', validationResult, allRows, onSelectRow,
    );
    ValidationResultsActions.createTestRowIfExists(
      'data_quality', 'Special Values', validationResult, allRows, onSelectRow,
    );
    ValidationResultsActions.createTestRowIfExists('min', 'Min', validationResult, allRows, onSelectRow);
    ValidationResultsActions.createTestRowIfExists('max', 'Max', validationResult, allRows, onSelectRow);
    return allRows;
  },

  getSchemaRows: validationTestResult => {
    const header = [
      <tr key="header" className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
        <th>Attribute Name</th>
        <th>Data Type</th>
        <th>Issue Type</th>
        <th>Validation Outcome</th>
      </tr>,
    ];

    const rows = validationTestResult.schema.details_by_attribute.map((test, ind) => {
      const issueType = test.issue_type ? test.issue_type : 'N/A';
      return (
        // eslint-disable-next-line react/no-array-index-key
        <tr key={ind} className="validation-results-test-pane-table-row">
          <th><OverflowTooltip text={test.attribute_name} /></th>
          <th><OverflowTooltip text={test.data_type} /></th>
          <th><OverflowTooltip text={issueType} /></th>
          <th className={`validation-outcome-${test.validation_outcome}`}>
            <OverflowTooltip text={test.validation_outcome} />
          </th>
        </tr>
      );
    });
    return header.concat(rows);
  },

  getPopShiftRows: validationTestResult => {
    const header = [
      <tr key="header" className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
        <th>Attribute Name</th>
        <th>Distribution Shift</th>
        <th>Measure Type</th>
        <th>Validation Outcome</th>
      </tr>,
    ];

    const rows = validationTestResult.population_shift.details_by_attribute.map((test, ind) => {
      let measureType = 'L-infinity' in test ? 'L-infinity' : 'PSI';
      let distShift = measureType === 'L-infinity' ? test['L-infinity'] : test.PSI;
      let validationOutcome = test.validation_outcome;

      if (distShift === null) {
        distShift = 'N/A';
      }

      if (test.validation_outcome === null) {
        distShift = 'N/A';
        measureType = 'N/A';
        validationOutcome = 'N/A';
      }
      return (
        // eslint-disable-next-line react/no-array-index-key
        <tr key={ind} className="validation-results-test-pane-table-row">
          <th><OverflowTooltip text={test.attribute_name} /></th>
          <th><OverflowTooltip text={distShift} /></th>
          <th><OverflowTooltip text={measureType} /></th>
          <th className={`validation-outcome-${validationOutcome}`}>
            <OverflowTooltip text={validationOutcome} />
          </th>
        </tr>
      );
    });
    return header.concat(rows);
  },

  getSpecialValuesRows: validationTestResult => {
    const header = [
      <tr key="header" className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
        <th>Attribute Name</th>
        <th>Value</th>
        <th>Expected (%)</th>
        <th>Actual (%)</th>
        <th>Difference</th>
        <th>Validation Outcome</th>
      </tr>,
    ];
    const rows = validationTestResult.data_quality.details_by_attribute.map((test, ind) => (
      // eslint-disable-next-line react/no-array-index-key
      <tr key={ind} className="validation-results-test-pane-table-row">
        <th><OverflowTooltip text={test.attribute_name} /></th>
        <th><OverflowTooltip text={test.value} /></th>
        <th><OverflowTooltip text={CommonActions.decimalToPercentage(test.pct_in_reference_data)} /></th>
        <th><OverflowTooltip text={CommonActions.decimalToPercentage(test.pct_in_current_data)} /></th>
        <th><OverflowTooltip text={CommonActions.decimalToPercentage(test.difference_in_pct)} /></th>
        <th className={`validation-outcome-${test.validation_outcome}`}>
          <OverflowTooltip text={test.validation_outcome} />
        </th>
      </tr>
    ));
    return header.concat(rows);
  },

  getMinRows: validationTestResult => {
    const header = [
      <tr key="header" className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
        <th>Attribute Name</th>
        <th>Expected Lower Bound</th>
        <th>Actual Minimum Value</th>
        <th>Percentage out of Bounds</th>
        <th>Validation Outcome</th>
      </tr>,
    ];

    const rows = validationTestResult.min.details_by_attribute.map((test, ind) => {
      const outOfBounds = (
        'percentage_out_of_bounds' in test
          ? CommonActions.decimalToPercentage(test.percentage_out_of_bounds)
          : 'N/A'
      );
      return (
        // eslint-disable-next-line react/no-array-index-key
        <tr key={ind} className="validation-results-test-pane-table-row">
          <th><OverflowTooltip text={test.attribute_name} /></th>
          <th><OverflowTooltip text={test.lower_bound} /></th>
          <th><OverflowTooltip text={test.min_value} /></th>
          <th><OverflowTooltip text={outOfBounds} /></th>
          <th className={`validation-outcome-${test.validation_outcome}`}>
            <OverflowTooltip text={test.validation_outcome} />
          </th>
        </tr>
      );
    });
    return header.concat(rows);
  },

  getMaxRows: validationTestResult => {
    const header = [
      <tr key="header" className="validation-results-test-pane-table-header validation-results-test-pane-table-row">
        <th>Attribute Name</th>
        <th>Expected Upper Bound</th>
        <th>Actual Maximum Value</th>
        <th>Percentage out of Bounds</th>
        <th>Validation Outcome</th>
      </tr>,
    ];

    const rows = validationTestResult.max.details_by_attribute.map((test, ind) => {
      const outOfBounds = (
        'percentage_out_of_bounds' in test
          ? CommonActions.decimalToPercentage(test.percentage_out_of_bounds)
          : 'N/A'
      );
      return (
        // eslint-disable-next-line react/no-array-index-key
        <tr key={ind} className="validation-results-test-pane-table-row">
          <th><OverflowTooltip text={test.attribute_name} /></th>
          <th><OverflowTooltip text={test.upper_bound} /></th>
          <th><OverflowTooltip text={test.max_value} /></th>
          <th><OverflowTooltip text={outOfBounds} /></th>
          <th className={`validation-outcome-${test.validation_outcome}`}>
            <OverflowTooltip text={test.validation_outcome} />
          </th>
        </tr>
      );
    });
    return header.concat(rows);
  },

  getTestTableRows: validationTestResult => {
    const testType = Object.keys(validationTestResult)[0];

    if (testType === 'schema') {
      return ValidationResultsActions.getSchemaRows(validationTestResult);
    }
    if (testType === 'population_shift') {
      return ValidationResultsActions.getPopShiftRows(validationTestResult);
    }
    if (testType === 'data_quality') {
      return ValidationResultsActions.getSpecialValuesRows(validationTestResult);
    }
    if (testType === 'min') {
      return ValidationResultsActions.getMinRows(validationTestResult);
    }
    if (testType === 'max') {
      return ValidationResultsActions.getMaxRows(validationTestResult);
    }
    return [];
  },

  getOverviewForAttribute: (validationResult, projectName, attribute) => {
    const url = `projects/${projectName}/monitors/${validationResult.monitor_package}/contracts/${validationResult.data_contract}/summary?inference_period=${validationResult.date}&attribute=${attribute}`; // eslint-disable-line max-len

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return [];
      });
  },
};

export default ValidationResultsActions;
