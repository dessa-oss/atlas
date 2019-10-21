import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsOverview extends Component {
  render() {
    return (
      <div className="validation-results-overview">
        <div className="overview-summary">
          <h2>Overview</h2>
          <h3>input_contract_3</h3>
          <ul>
            <li>
              <div className="summary-key">Monitor Name:</div>
              <div className="summary-value">monitor_1</div>
            </li>
            <li>
              <div className="summary-key">Job ID:</div>
              <div className="summary-value">s8d97fs98</div>
            </li>
            <li>
              <div className="summary-key">Time:</div>
              <div className="summary-value">2019-08-22</div>
            </li>
            <li>
              <div className="summary-key">User:</div>
              <div className="summary-value">User</div>
            </li>
            <li>
              <div className="summary-key">Row count:</div>
              <div className="summary-value">1,111,111 1,222,213 (+9%)</div>
            </li>
          </ul>
        </div>
        <div className="overview-graph" />
        <div className="overview-graph-stats" />
      </div>
    );
  }
}

ValidationResultsOverview.propTypes = {
};

ValidationResultsOverview.defaultProps = {
};

export default ValidationResultsOverview;
