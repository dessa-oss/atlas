import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import MonitorListTable from "./MonitorListTable";
import ScheduleDetails from "./ScheduleDetails";
import MonitorLogsModal from "./MonitorLogsModal";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";

class MonitorSchedules extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedMonitor: null,
      logsModalIsOpen: false,
      logsModalJobID: null,
      allMonitors: {}
    };

    this.selectRow = this.selectRow.bind(this);
    this.reload = this.reload.bind(this);
    this.toggleLogsModal = this.toggleLogsModal.bind(this);
  }

  selectRow(selectedItem) {
    this.setState({ selectedMonitor: selectedItem });
  }

  componentDidMount() {
    this.reload();
  }

  async reload() {
    const { location } = this.props;

    if (location) {
      const projectName = location.state.project.name;
      const monitorResult = await MonitorSchedulesActions.getMonitorList(projectName);
      this.setState({ allMonitors: monitorResult });
    }
  }

  toggleLogsModal(logsModalJobID) {
    const { logsModalIsOpen } = this.state;
    this.setState({ logsModalIsOpen: !logsModalIsOpen, logsModalJobID: logsModalJobID });
  }

  render() {
    const {
      selectedMonitor,
      logsModalIsOpen,
      logsModalJobID,
      allMonitors
    } = this.state;
    const { location } = this.props;

    return (
      <Layout tab="Schedules" title="Data Health">
        <div className="monitor-schedules-container">
          <h3 className="section-title">Monitor Schedules</h3>
          <div className="schedule-details">
            <MonitorListTable
              onClickRow={this.selectRow}
              selectedRow={selectedMonitor}
              allMonitors={allMonitors}
              reload={this.reload}
            />
            <ScheduleDetails
              location={location}
              selectedMonitor={selectedMonitor}
              toggleLogsModal={this.toggleLogsModal}
              reload={this.reload}
              allMonitors={allMonitors}
            />
            <MonitorLogsModal
              isOpen={logsModalIsOpen}
              toggle={this.toggleLogsModal}
              jobID={logsModalJobID}
              projectName={location.state.project.name}
            />
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
