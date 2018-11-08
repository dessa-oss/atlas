import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ProjectSummary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      project: this.props.project,
    };
  }

  render() {
    const { project } = this.state;
    return (
      <div className="project-summary-container">
        <div className="project-summary-info-container">
          <p className="project-summary-name-text">{project.name}</p>
          <p className="project-summary-source-text">{project.source}</p>
          <p className="project-summary-owner-text">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="project-summary-created-at-text">
            Created at: <span>{project.created_at}</span>
          </p>
          <div className="project-summary-button-container">
            <button type="button" className="project-view-queue text-upper">view queue</button>
            <button type="button" className="project-view-job-list text-upper">view job list</button>
          </div>
        </div>
        <div className="project-summary-metrics-container" />
      </div>
    );
  }
}

ProjectSummary.propTypes = {
  project: PropTypes.object,
};

ProjectSummary.defaultProps = {
  project: {},
};

export default ProjectSummary;
