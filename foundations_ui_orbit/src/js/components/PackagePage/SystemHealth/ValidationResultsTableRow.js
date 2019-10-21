import React, { Component } from "react";
import moment from "moment";
import PropTypes from "prop-types";

class ValidationResultsTableRow extends Component {
  constructor(props) {
    super(props);

    this.state = {
      time: this.props.time,
      monitorName: this.props.monitorName,
      contractName: this.props.contractName,
      numCritical: this.props.numCritical
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

    return (
      time === selectedRow.time
      && monitorName === selectedRow.monitorName
      && contractName === selectedRow.contractName
      && numCritical === selectedRow.numCritical
    );
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

    return (
      <div className={`validation-results-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="val-time-table-cell">{date}</div>
        <div className="val-monitor-table-cell">{monitorName}</div>
        <div className="val-contract-table-cell">{contractName}</div>
        <div className="val-critical-table-cell">{numCritical}</div>
      </div>
    );
  }
}

ValidationResultsTableRow.propTypes = {
  time: PropTypes.string,
  monitorName: PropTypes.string,
  contractName: PropTypes.string,
  numCritical: PropTypes.string,
  onClick: PropTypes.func,
  selectedRow: PropTypes.object
};

ValidationResultsTableRow.defaultProps = {
  time: "Invalid date",
  monitorName: "Invalid monitor name",
  contractName: "Invalid contract name",
  numCritical: "0",
  onClick: () => {},
  selectedRow: {}
};


export default ValidationResultsTableRow;
