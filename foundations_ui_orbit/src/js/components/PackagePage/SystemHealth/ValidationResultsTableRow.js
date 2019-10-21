import React, { Component } from "react";
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

  render() {
    const {
      time,
      monitorName,
      contractName,
      numCritical
    } = this.state;

    return (
      <div className="validation-results-table-row" onClick={this.onClick}>
        <div className="val-time-table-cell">{time}</div>
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
  onClick: PropTypes.func
};

ValidationResultsTableRow.defaultProps = {
  time: "Invalid date",
  monitorName: "Invalid monitor name",
  contractName: "Invalid contract name",
  numCritical: "0",
  onClick: () => {}
};


export default ValidationResultsTableRow;
