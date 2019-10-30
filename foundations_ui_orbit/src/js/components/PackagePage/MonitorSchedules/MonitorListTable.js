import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";

class MonitorListTable extends Component {
  constructor(props) {
    super(props);
    const { location } = this.props;

    this.state = {
      rows: null,
      projectName: location.state.project.name
    };
    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  async reload() {
    const { projectName } = this.state;
    const { onClickRow, reload } = this.props;

    const result = await MonitorSchedulesActions.getMonitorList(projectName);
    const rows = MonitorSchedulesActions.getRows(result, onClickRow);
    this.setState({ rows: rows });
    reload();
  }

  render() {
    const { rows } = this.state;
    const { selectedRow } = this.props;

    console.log("selected row: ", selectedRow);

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
  location: PropTypes.object,
  onClickRow: PropTypes.func,
  selectedRow: PropTypes.object,
  reload: PropTypes.func
};

MonitorListTable.defaultProps = {
  location: { state: {} },
  onClickRow: () => {},
  selectedRow: {},
  reload: () => {}
};

export default MonitorListTable;
