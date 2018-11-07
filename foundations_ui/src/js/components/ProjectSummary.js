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
          <div className="project-summary-name">
            <p className="project-summary-name-text">{project.name}</p>
          </div>
          <div className="project-summary-source">
            <p className="project-summary-source-text">{project.source}</p>
          </div>
          <div className="project-summary-owner">
            <p className="project-summary-owner-text">Project owner:</p>
            <p className="project-summary-owner-name-text">{project.owner}</p>
          </div>
          <div className="project-summary-created-at">
            <p className="project-summary-created-at-text">Created at: </p>
            <p className="project-summary-created-time-text">{project.created_at}</p>
          </div>
          <div className="project-summary-button-container">
            <button type="button" className="project-view-queue">VIEW QUEUE</button>
            <button type="button" className="project-view-job-list">VIEW JOB LIST</button>
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
