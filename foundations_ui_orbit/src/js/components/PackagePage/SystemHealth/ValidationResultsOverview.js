import React, { Component } from "react";
import moment from "moment";
import PropTypes from "prop-types";

class ValidationResultsOverview extends Component {
  render() {
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");
    const sign = validationResult.row_count.row_count_diff >= 0 ? "+" : "-";
    const rowDiff = Math.round(Math.abs(validationResult.row_count.row_count_diff) * 1000) / 1000;
    const rowCount = `${validationResult.row_count.expected_row_count} -> ${validationResult.row_count.actual_row_count} (${sign}${rowDiff}%)`; // eslint-disable-line max-len

    return (
      <div className="validation-results-overview">
        <div className="overview-summary">
          <div className="overview-summary-center">
            <div className="overview-heading font-bold">Overview</div>
            <div className="overview-contract-container">
              <div className="overview-contract-name">{validationResult.data_contract}</div>
              <div className="i--icon-open" />
            </div>
            <div className="overview-labels font-bold">
              Monitor Name:<br />
              Job ID:<br />
              Time:<br />
              User:<br />
              Row count:
            </div>
            <div className="overview-values">
              {validationResult.monitor_package}<br />
              some-job-id<br />
              {date}<br />
              some-user<br />
              {rowCount}
            </div>
          </div>
        </div>
        <div className="overview-graph" />
        <div className="overview-graph-stats" />
      </div>
    );
  }
}

ValidationResultsOverview.propTypes = {
  validationResult: PropTypes.object
};

ValidationResultsOverview.defaultProps = {
  validationResult: {}
};

export default ValidationResultsOverview;
