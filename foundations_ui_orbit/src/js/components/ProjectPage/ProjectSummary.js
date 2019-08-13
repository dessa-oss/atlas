import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";

class ProjectSummary extends Component {
  constructor(props) {
    super(props);
    this.viewClick = this.viewClick.bind(this);
    this.packageClick = this.packageClick.bind(this);
    this.state = {
      tab: props.tab,
      project: this.props.project,
      selectProject: this.props.selectProject
    };
  }

  viewClick() {
    const { project, selectProject } = this.state;
    selectProject(project);
  }

  packageClick() {
    this.setState({
      tab: "Management"
    });

    this.props.history.push(
      "/projects/" + this.state.project.name + "/management",
      {
        project: this.state.project
      }
    );
  }

  render() {
    const { project } = this.state;
    return (
      <div
        className="project-summary-container elevation-1"
        onClick={this.packageClick}
      >
        <div className="project-summary-info-container">
          <h2 className="font-bold">{project.name}</h2>
          <p>Data Source: Unknown</p>
          <p className="font-bold">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="font-bold">
            Created at: <span>{project.created_at}</span>
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
