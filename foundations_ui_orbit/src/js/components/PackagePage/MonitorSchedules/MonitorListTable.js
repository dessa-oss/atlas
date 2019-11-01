import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import CommonActions from "../../../actions/CommonActions";

class MonitorListTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      rows: null
    };
    this.reload = this.reload.bind(this);
  }

  componentDidUpdate(prevProps) {
    const { allMonitors } = this.props;

    if (!CommonActions.deepEqual(prevProps.allMonitors, allMonitors)) {
      this.reload();
    }
  }

  async reload() {
    const { onClickRow, allMonitors } = this.props;

    const rows = MonitorSchedulesActions.getRows(allMonitors, onClickRow);
    this.setState({ rows: rows });
  }

  render() {
    const { rows } = this.state;
    const { selectedRow } = this.props;

    let rowsWithProps = [];
    if (rows) {
      rowsWithProps = rows.map(row => React.cloneElement(
        row,
        { selectedRow: selectedRow }
      ));
    }

    return (
      <div>
        {/* <div className="i--icon-refresh" onClick={this.reload} /> */}
        <div className="monitor-listing">
          <div className="monitor-items">
            <div className="monitor-table-row" onClick={this.onClick}>
              <div className="monitor-table-cell">Monitor Name</div>
              <div className="monitor-status-table-cell">Status</div>
              <div className="monitor-user-table-cell">User</div>
            </div>
            {rowsWithProps}
          </div>
        </div>
      </div>
    );
  }
}

MonitorListTable.propTypes = {
  onClickRow: PropTypes.func,
  selectedRow: PropTypes.string,
  reload: PropTypes.func,
  allMonitors: PropTypes.object
};

MonitorListTable.defaultProps = {
  onClickRow: () => {},
  selectedRow: "",
  reload: () => {},
  allMonitors: {}
};

export default MonitorListTable;
