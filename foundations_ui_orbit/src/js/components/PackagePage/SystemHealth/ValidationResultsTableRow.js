import React, { Component } from "react";
import moment from "moment";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";
import OverflowTooltip from "../../common/OverflowTooltip";

class ValidationResultsTableRow extends Component {
  constructor(props) {
    super(props);
    const {
      time, monitorName, contractName, numCritical
    } = this.props;

    this.state = {
      time: time,
      monitorName: monitorName,
      contractName: contractName,
      numCritical: numCritical
    };

    this.onClick = this.onClick.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
  }

  onClick() {
    const {
      time,
      monitorName,
      contractName,
      numCritical
    } = this.state;
    const { onClick } = this.props;

    onClick({
      time: time,
      monitorName: monitorName,
      contractName: contractName,
      numCritical: numCritical
    });
  }

  isSelectedRow() {
    const {
      time,
      monitorName,
      contractName,
      numCritical
    } = this.state;
    const { selectedRow } = this.props;
    const thisRow = {
      time: time,
      monitorName: monitorName,
      contractName: contractName,
      numCritical: numCritical
    };

    return CommonActions.deepEqual(thisRow, selectedRow);
  }

  render() {
    const {
      time,
      monitorName,
      contractName,
      numCritical
    } = this.state;

    const selectedClass = this.isSelectedRow() ? "selected-row" : "";
    const date = moment(time).format("YYYY-MM-DD").toString();
    const criticalState = numCritical > 0 ? "critical" : "healthy";
    const numCriticalVal = numCritical > 0 ? numCritical : "";

    return (
      <div className={`validation-results-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="val-time-table-cell">
          <OverflowTooltip text={date} />
        </div>
        <div className="val-monitor-table-cell">
          <OverflowTooltip text={monitorName} />
        </div>
        <div className="val-contract-table-cell">
          <OverflowTooltip text={contractName} />
        </div>
        <div className="val-critical-table-cell">
          <div className={`val-critical-table-cell-${criticalState}`}>
            {numCriticalVal}
          </div>
        </div>
      </div>
    );
  }
}

ValidationResultsTableRow.propTypes = {
  time: PropTypes.string,
  monitorName: PropTypes.string,
  contractName: PropTypes.string,
  numCritical: PropTypes.number,
  onClick: PropTypes.func,
  selectedRow: PropTypes.object
};

ValidationResultsTableRow.defaultProps = {
  time: "Invalid date",
  monitorName: "Invalid monitor name",
  contractName: "Invalid contract name",
  numCritical: 0,
  onClick: () => {},
  selectedRow: {}
};


export default ValidationResultsTableRow;
