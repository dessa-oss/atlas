import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";

const SideBar = props => {
  const onClickDeployment = () => {
    props.history.push("/deployment", {
      project: props.location.state.project
    });
  };

  const onClickEvaluation = () => {
    props.history.push(
      "/projects/" + props.location.state.project.name + "/evaluation",
      {
        project: props.location.state.project
      }
    );
  };

  const onClickPerformance = () => {
    props.history.push("/performance", {
      project: props.location.state.project
    });
  };

  const onClickDashboard = () => {
    props.history.push("/", {
      project: props.location.state.project
    });
  };

  const onClickTimeline = () => {
    props.history.push("/timeline", {
      project: props.location.state.project
    });
  };

  const onClickSettings = () => {
    props.history.push(
      "/projects/" + props.location.state.project.name + "/settings",
      {
        project: props.location.state.project
      }
    );
  };

  const onClickModelManagement = () => {
    props.history.push(
      "/projects/" + props.location.state.project.name + "/management",
      {
        project: props.location.state.project
      }
    );
  };

  const onClickHealth = () => {
    props.history.push(
      "/projects/" + props.location.state.project.name + "/health",
      {
        project: props.location.state.project
      }
    );
  };

  return (
    <div className="sidebar">
      <div onClick={onClickDashboard} className="sidebar-item icon-home">
        <div class="label">Dashboard</div>
      </div>
      {/* <div
        onClick={onClickTimeline}
        className={
          props.tab === "Timeline"
            ? "sidebar-item active  icon-three-dots-blue"
            : "sidebar-item icon-three-dots"
        }
      >
        <div class="label">History</div>
      </div> */}
      <div
        onClick={onClickEvaluation}
        className={
          props.tab === "Evaluation"
            ? "sidebar-item active icon-chart-blue"
            : "sidebar-item icon-chart"
        }
      >
        <div class="label model-eval">
          Model
          <br />
          Evaluation
        </div>
      </div>
      <div
        onClick={onClickHealth}
        className={
          props.tab === "Health"
            ? "sidebar-item active icon-monitor-blue"
            : "sidebar-item icon-monitor"
        }
      >
        <div class="label">Data Health</div>
      </div>
      {/* <div
        onClick={onClickDeployment}
        className={
          props.tab === "Deployment"
            ? "sidebar-item active icon-cloud-blue"
            : "sidebar-item icon-cloud"
        }
      >
        <div class="label">Deployment</div>
      </div> */}
      <div
        onClick={onClickModelManagement}
        className={
          props.tab === "Management"
            ? "sidebar-item active icon-table-blue"
            : "sidebar-item icon-table"
        }
      >
        <div class="label">Model Management</div>
      </div>
      <div
        onClick={onClickSettings}
        className={
          props.tab === "Settings"
            ? "sidebar-item active icon-gear-blue"
            : "sidebar-item icon-gear"
        }
      >
        <div class="label settings">Settings</div>
      </div>
    </div>
  );
};

SideBar.propTypes = {
  tab: PropTypes.string,

  history: PropTypes.object,
  project: PropTypes.object
};

SideBar.defaultProps = {
  tab: "Deployment"
};

export default withRouter(SideBar);
