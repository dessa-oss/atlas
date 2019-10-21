import React from "react";
import { get, post } from "./BaseActions";
import ValidationResultsTableRow from "../components/PackagePage/SystemHealth/ValidationResultsTableRow";

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

  getRows: (results, onClickRow) => {
    return results.map(result => {
      const key = result.inference_period + result.model_package + result.data_contract;
      return (
        <ValidationResultsTableRow
          key={key}
          onClick={onClickRow}
          time={result.inference_period}
          monitorName={result.model_package}
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
  }
};

export default ValidationResultsActions;
