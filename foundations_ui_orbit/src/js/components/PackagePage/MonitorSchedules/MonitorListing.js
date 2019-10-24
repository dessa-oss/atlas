import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import MonitorOverview from "./MonitorOverview";

class MonitorListing extends Component {
  render() {
    const { selectedValidationResult } = this.props;
    let test = "test";
    if (selectedValidationResult) {
      test = selectedValidationResult.time
      + selectedValidationResult.monitorName
      + selectedValidationResult.contractName;
    }

    return (
      <div className="monitor-jobs">
        <h3>Monitor Listing</h3>
      </div>
    );
  }
}

MonitorListing.propTypes = {
  selectedValidationResult: PropTypes.object
};

MonitorListing.defaultProps = {
  selectedValidationResult: {}
};

export default MonitorListing;
