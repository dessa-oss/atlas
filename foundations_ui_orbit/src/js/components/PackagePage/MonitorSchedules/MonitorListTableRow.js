import React, { Component } from "react";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";


class MonitorListTableRow extends Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
    this.isSelectedRow = this.isSelectedRow.bind(this);
  }

  onClick() {
    const {
      onClick,
      monitorName,
      status,
      user
    } = this.props;

    onClick({
      monitorName: monitorName,
      status: status,
      user: user
    });
  }

  isSelectedRow() {
    const {
      selectedRow,
      monitorName,
      status,
      user
    } = this.props;
    const thisRow = {
      monitorName: monitorName,
      status: status,
      user: user
    };

    return CommonActions.deepEqual(thisRow, selectedRow);
  }

  render() {
    const {
      monitorName,
      status,
      user
    } = this.props;

    const selectedClass = this.isSelectedRow() ? "selected-row" : "";

    function addStatus(rowStatus) {
      if (rowStatus === "paused") {
        return <div className="status-icon status-paused-orange" />;
      }

      if (rowStatus === "active") {
        return <div className="status-icon status-green" />;
      }
    }

    const statusIcon = addStatus(status);

    return (
      <div className={`monitor-table-row ${selectedClass}`} onClick={this.onClick}>
        <div className="monitor-table-cell">{monitorName}</div>
        <div className="monitor-status-table-cell">{statusIcon}</div>
        <div className="monitor-user-table-cell">{user}</div>
      </div>
    );
  }
}

MonitorListTableRow.propTypes = {
  monitorName: PropTypes.string,
  status: PropTypes.string,
  user: PropTypes.string,
  onClick: PropTypes.func,
  selectedRow: PropTypes.object
};

MonitorListTableRow.defaultProps = {
  monitorName: "Invalid monitor name",
  status: "Invalid contract name",
  user: "",
  onClick: () => {},
  selectedRow: PropTypes.object
};


export default MonitorListTableRow;
