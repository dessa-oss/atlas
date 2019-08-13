import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";

const ProjectSummary = props => {

  const viewClick = () => {
    props.selectProject(props.project);
  }

  const packageClick = () => {
    props.history.push(
      "/projects/" + props.project.name + "/management",
      {
        project: props.project
      }
    );
  }

    return (
      <div
        className="project-summary-container elevation-1"
        onClick={packageClick}
      >
        <div className="project-summary-info-container">
          <h2 className="font-bold">{props.project.name}</h2>
          <p>Data Source: Unknown</p>
          <p className="font-bold">
            Project owner: <span>{props.project.owner}</span>
          </p>
          <p className="font-bold">
            Created at: <span>{props.project.created_at}</span>
          </p>
          <div className="project-summary-button-container">
            {/* <button type="button" className="b--mat b--affirmative">
              view queue
            </button>
            <button type="button" className="b--mat b--affirmative">
              view job list
            </button> */}
            {/* <button
              type="button"
              onClick={this.packageClick}
              className="b--mat b--affirmative"
            >
              Post Deploy Management
            </button> */}
          </div>
        </div>
        <div className="project-summary-metrics-container" />
      </div>
    );
  
}

ProjectSummary.propTypes = {
  project: PropTypes.object,
  selectProject: PropTypes.func
};

ProjectSummary.defaultProps = {
  project: {},
  selectProject: () => null
};

export default withRouter(ProjectSummary);
