import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import { get, post } from "../../../actions/BaseActions";
import PropTypes from "prop-types";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import MonitorListTable from "./MonitorListTable";
import ScheduleDetails from "./ScheduleDetails";

class MonitorSchedules extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedMonitor: {}
    };
    this.selectRow = this.selectRow.bind(this);
    this.reload = this.reload.bind(this);
  }

  selectRow(selectedItem) {
    this.setState({ selectedMonitor: selectedItem });
  }

  reload() {
    this.setState({ selectedMonitor: {} });
  }

  render() {
    const { selectedMonitor } = this.state;

    const location = this.props.location;

    return (
      <Layout tab="Schedules" title="Data Health">
        <div className="monitor-schedules-container">
          <h3 className="section-title">Monitor Schedules</h3>
          <div className="schedule-details">
            <MonitorListTable location={location} onClickRow={this.selectRow} selectedRow={selectedMonitor} />
            <ScheduleDetails location={location} selectedMonitor={selectedMonitor} />
          </div>
        </div>
      </Layout>
    );
  }
}

MonitorSchedules.propTypes = {
  location: PropTypes.object
};

MonitorSchedules.defaultProps = {
  location: { state: {} }
};

export default withRouter(MonitorSchedules);
