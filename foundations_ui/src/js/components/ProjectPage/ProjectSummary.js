import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ProjectSummary extends Component {
  constructor(props) {
    super(props);
    this.viewClick = this.viewClick.bind(this);
    this.state = {
      project: this.props.project,
      selectProject: this.props.selectProject,
    };
  }

  viewClick() {
    const { project, selectProject } = this.state;
    selectProject(project.name);
  }

  render() {
    const { project } = this.state;
    return (
      <div className="project-summary-container elevation-1">
        <div className="project-summary-info-container">
          <h2 className="project-summary-name-text font-bold">{project.name}</h2>
          <p className="project-summary-source-text">Data Source: Unknown</p>
          <p className="project-summary-owner-text font-bold">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="project-summary-created-at-text font-bold">
            Created at: <span>{project.created_at}</span>
          </p>
          <div className="project-summary-button-container">
            <button type="button" className="b--mat b--affirmative">view queue</button>
            <button type="button" onClick={this.viewClick} className="b--mat b--affirmative">view job list</button>
          </div>
        </div>
        <div className="project-summary-metrics-container" />
      </div>
    );
  }
}

ProjectSummary.propTypes = {
  project: PropTypes.object,
  selectProject: PropTypes.func,
};

ProjectSummary.defaultProps = {
  project: {},
  selectProject: () => null,
};

export default ProjectSummary;
