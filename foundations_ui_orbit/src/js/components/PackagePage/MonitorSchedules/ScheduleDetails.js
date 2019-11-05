import React, { Component } from "react";
import PropTypes from "prop-types";
import MonitorOverview from "./MonitorOverview";
import MonitorJobsTable from "./MonitorJobsTable";
import CommonActions from "../../../actions/CommonActions";

class ScheduleDetails extends Component {
  constructor(props) {
    super(props);

    this.state = {
      monitorResult: {}
    };

    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    const { selectedMonitor, allMonitors } = this.props;
    if (selectedMonitor !== prevProps.selectedMonitor
      || !CommonActions.deepEqual(allMonitors, prevProps.allMonitors)) {
      this.reload();
    }
  }

  async reload() {
    const { selectedMonitor, allMonitors } = this.props;

    if (selectedMonitor) {
      this.setState({ monitorResult: allMonitors[selectedMonitor] });
    } else {
      this.setState({ monitorResult: {} });
    }
  }

  render() {
    const { monitorResult } = this.state;
    const {
      location,
      toggleLogsModal,
      reload,
      toggleDeleteModal
    } = this.props;

    let mainRender = (
      <div className="right-side">
        <div className="monitor-summary">
          <MonitorOverview monitorResult={monitorResult} reload={reload} toggleDeleteModal={toggleDeleteModal} />
          <MonitorJobsTable location={location} monitorResult={monitorResult} toggleLogsModal={toggleLogsModal} />
        </div>
      </div>
    );
    if (!monitorResult || CommonActions.isEmptyObject(monitorResult)) {
      mainRender = (
        <div className="right-side">
          <div className="monitor-summary">
            <div className="monitor-details-empty-state">
              <div className="i--icon-clipboard" />
              <div className="monitor-details-empty-state-text">
                Click on a monitor to see its details.
              </div>
            </div>
          </div>
        </div>
      );
    }

    return mainRender;
  }
}

ScheduleDetails.propTypes = {
  location: PropTypes.object,
  selectedMonitor: PropTypes.string,
  toggleLogsModal: PropTypes.func,
  toggleDeleteModal: PropTypes.func,
  allMonitors: PropTypes.object,
  reload: PropTypes.func
};

ScheduleDetails.defaultProps = {
  location: {},
  selectedMonitor: "",
  toggleLogsModal: () => {},
  toggleDeleteModal: () => {},
  allMonitors: {},
  reload: () => {}
};

export default ScheduleDetails;
