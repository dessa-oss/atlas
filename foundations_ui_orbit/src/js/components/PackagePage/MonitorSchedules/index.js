import React from "react";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import { get, post } from "../../../actions/BaseActions";
import PropTypes from "prop-types";
import moment from "moment";
import ModalTutorial from "../../common/ModalTutorial";

const MonitorSchedules = props => {
  const [tutorialVisible, setTutorialVisible] = React.useState(false);

  const onToggleTutorial = () => {
    let value = !tutorialVisible;
    setTutorialVisible(value);
  };

  const reload = () => {
    const { location } = props;

    get(`projects/${location.state.project.name}/validation_report_list`).then(result => {
      if (result) {
        let entries = [];
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  // data != undefined ?
  const mainWindow = (
    <Layout tab="Health" title="Data Health" openTutorial={onToggleTutorial}>
      <div className="monitor-schedules-container">
        <h3 className="section-title">Monitor Schedules</h3>
        <h4>Refresh</h4>
        <div className="schedule-details">
          <div className="monitor-listing">
            <ul>
              <li>
                <div className="monitor-name">Monitor Name</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
              <li>
                <div className="monitor-name">Monitor_1</div>
                <div className="monitor-status">Status</div>
                <div className="monitor-user">User</div>
              </li>
            </ul>
          </div>
          <div className="monitor-summary">
            <div className="monitor-info">
              <div className="monitor-overview">
                <h3>Overview</h3>
              </div>
              <div className="monitor-details">
                <h3>Details</h3>
              </div>
              <div className="monitor-calendar">
                <h3>Calendar</h3>
              </div>
            </div>
            <div className="monitor-jobs-heading">
              <h3>Monitor Jobs</h3>
            </div>
            <div className="monitor-jobs">
              <ul>
                <li>listing one</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );

  return <div>{mainWindow}</div>;
};

MonitorSchedules.propTypes = {
  location: PropTypes.object
};

MonitorSchedules.defaultProps = {
  location: { state: {} }
};

export default withRouter(MonitorSchedules);
