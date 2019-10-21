import React from "react";
import { get, post } from "./BaseActions";
import ValidationResultsTableRow from "../components/PackagePage/SystemHealth/ValidationResultsTableRow";
import ValidationResultsTestsListRow from "../components/PackagePage/SystemHealth/ValidationResultsTestListRow";

const ValidationResultsActions = {
  getValidationResultList: projectName => {
    const url = `projects/${projectName}/validation_report_list`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(error => {
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
          numCritical={2}
        />
      );
    });
  },

  getValidationResults: (projectName, inferencePeriod, monitorPackage, dataContract) => {
    const url = `projects/${projectName}/validation_results`;
    const body = {
      inference_period: inferencePeriod,
      monitor_package: monitorPackage,
      data_contract: dataContract
    };

    return post(url, body)
      .then(results => {
        return results;
      })
      .catch(error => {
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
        />
      );
    }
  },

  getTestRows: (validationResult, onSelectRow) => {
    const allRows = [];
    ValidationResultsActions.createTestRowIfExists("schema", "Schema Check", validationResult, allRows, onSelectRow);
    ValidationResultsActions.createTestRowIfExists(
      "population_shift", "Population Shift", validationResult, allRows, onSelectRow
    );
    ValidationResultsActions.createTestRowIfExists(
      "data_quality", "Special Values", validationResult, allRows, onSelectRow
    );
    ValidationResultsActions.createTestRowIfExists("min", "Min", validationResult, allRows, onSelectRow);
    ValidationResultsActions.createTestRowIfExists("max", "Max", validationResult, allRows, onSelectRow);
    return allRows;
  }
};

export default ValidationResultsActions;
