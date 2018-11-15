import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(allInputParams) {
    let inputParams = null;
    if (allInputParams.length > 0) {
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(<JobColumnHeader key={key} title={input} className="inline-block" containerClass="input-metric-column-header" />);
      });
    }
    return inputParams;
  }
}

export default CommonActions;
