import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";

const SideBar = props => {
  const onClickDeployment = () => {
    const { history, location } = props;

    history.push(`/projects/${location.state.project.name}/deployment`, {
      project: location.state.project
    });
  };

  const onClickEvaluation = () => {
    const { history, location } = props;

    history.push(
      `/projects/${location.state.project.name}/evaluation`,
      {
        project: location.state.project
      }
    );
  };

  const onClickDashboard = () => {
    const { history, location } = props;

    history.push("/", {
      project: location.state.project
    });
  };

  const onClickTimeline = () => {
    const { history, location } = props;

    history.push(`/projects/${location.state.project.name}/timeline`, {
      project: location.state.project
    });
  };

  const onClickSettings = () => {
    const { history, location } = props;

    history.push(
      `/projects/${location.state.project.name}/settings`,
      {
        project: location.state.project
      }
    );
  };

  const onClickModelManagement = () => {
    const { history, location } = props;

    history.push(
      `/projects/${location.state.project.name}/management`,
      {
        project: location.state.project
      }
    );
  };

  const onClickHealth = () => {
    const { history, location } = props;

    history.push(
      `/projects/${location.state.project.name}/health`,
      {
        project: location.state.project
      }
    );
  };

  const { tab } = props;


  return (
    <div className="sidebar">
      <div onClick={onClickDashboard} className="sidebar-item icon-home">
        <div className="label">Dashboard</div>
      </div>
      <div
        onClick={onClickTimeline}
        className={
          tab === "Timeline"
            ? "sidebar-item active  icon-three-dots-blue"
            : "sidebar-item icon-three-dots"
        }
      >
        <div className="label">History</div>
      </div>
      <div
        onClick={onClickEvaluation}
        className={
          tab === "Evaluation"
            ? "sidebar-item active icon-chart-blue"
            : "sidebar-item icon-chart"
        }
      >
        <div className="label model-eval">
          Model
          <br />
          Evaluation
        </div>
      </div>
      <div
        onClick={onClickHealth}
        className={
          tab === "Health"
            ? "sidebar-item active icon-monitor-blue"
            : "sidebar-item icon-monitor"
        }
      >
        <div className="label">Data Health</div>
      </div>
      <div
        onClick={onClickDeployment}
        className={
          tab === "Deployment"
            ? "sidebar-item active icon-cloud-blue"
            : "sidebar-item icon-cloud"
        }
      >
        <div className="label">Deployment</div>
      </div>
      <div
        onClick={onClickModelManagement}
        className={
          tab === "Management"
            ? "sidebar-item active icon-table-blue"
            : "sidebar-item icon-table"
        }
      >
        <div className="label">Model Management</div>
      </div>
      <div
        onClick={onClickSettings}
        className={
          tab === "Settings"
            ? "sidebar-item active icon-gear-blue"
            : "sidebar-item icon-gear"
        }
      >
        <div className="label settings">Settings</div>
      </div>
    </div>
  );
};

SideBar.propTypes = {
  tab: PropTypes.string,
  history: PropTypes.object,
  location: PropTypes.object
};

SideBar.defaultProps = {
  tab: "Deployment",
  history: {},
  location: { state: {} }
};

export default withRouter(SideBar);
