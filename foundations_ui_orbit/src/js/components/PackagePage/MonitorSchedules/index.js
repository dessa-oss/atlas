import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import MonitorListTable from "./MonitorListTable";
import ScheduleDetails from "./ScheduleDetails";
import MonitorLogsModal from "./MonitorLogsModal";
import MonitorSchedulesActions from "../../../actions/MonitorSchedulesActions";
import DeleteConfirmModal from "./DeleteConfirmModal";
import Loading from "../../common/Loading";

class MonitorSchedules extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedMonitor: null,
      logsModalIsOpen: false,
      logsModalJobID: null,
      deleteModalIsOpen: false,
      allMonitors: {},
      isLoading: false
    };

    this.selectRow = this.selectRow.bind(this);
    this.reload = this.reload.bind(this);
    this.toggleLogsModal = this.toggleLogsModal.bind(this);
    this.toggleDeleteModal = this.toggleDeleteModal.bind(this);
    this.deleteCurrentMonitor = this.deleteCurrentMonitor.bind(this);
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

  toggleDeleteModal() {
    const { deleteModalIsOpen } = this.state;
    this.setState({ deleteModalIsOpen: !deleteModalIsOpen });
  }

  deleteCurrentMonitor() {
    const { allMonitors, selectedMonitor } = this.state;
    const { location } = this.props;

    this.setState({ isLoading: true }, async () => {
      const monitorName = allMonitors[selectedMonitor].properties.spec.environment.MONITOR_NAME;
      const projectName = location.state.project.name;
      await MonitorSchedulesActions.deleteMonitor(projectName, monitorName);
      const jobsObjects = await MonitorSchedulesActions.getMonitorJobs(projectName, monitorName);

      if (!("error" in jobsObjects)) {
        const jobs = jobsObjects.map(obj => obj.job_id);
        await MonitorSchedulesActions.deleteMonitorJobs(jobs, projectName, monitorName);
      }

      this.setState({ isLoading: false }, this.reload);
    });
  }

  render() {
    const {
      selectedMonitor,
      logsModalIsOpen,
      logsModalJobID,
      allMonitors,
      deleteModalIsOpen,
      isLoading
    } = this.state;
    const { location } = this.props;

    const loading = (
      isLoading
        ? <Loading loadingMessage="" floating />
        : null
    );

    return (
      <Layout tab="Schedules" title="Data Health">
        <div className="monitor-schedules-container">
          <div className="section-title font-bold">Monitor Schedules</div>
          <div className="schedule-details">
            {loading}
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
              toggleDeleteModal={this.toggleDeleteModal}
              reload={this.reload}
              allMonitors={allMonitors}
            />
            <MonitorLogsModal
              isOpen={logsModalIsOpen}
              toggle={this.toggleLogsModal}
              jobID={logsModalJobID}
              projectName={location.state.project.name}
            />
            <DeleteConfirmModal
              isOpen={deleteModalIsOpen}
              toggle={this.toggleDeleteModal}
              onConfirm={this.deleteCurrentMonitor}
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
