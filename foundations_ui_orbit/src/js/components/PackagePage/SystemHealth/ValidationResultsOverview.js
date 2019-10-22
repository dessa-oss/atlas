import React, { Component } from "react";
import moment from "moment";
import PropTypes from "prop-types";

class ValidationResultsOverview extends Component {
  render() {
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");

    return (
      <div className="validation-results-overview">
        <div className="overview-summary">
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
            some-row-count
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
