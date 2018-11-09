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
      <div className="project-summary-container elevation-1">
        <div className="project-summary-info-container">
          <h2 className="project-summary-name-text">{project.name}</h2>
          <p className="project-summary-source-text">data source</p>
          <p className="project-summary-owner-text">
            Project owner: <span className="font-regular">{project.owner}</span>
          </p>
          <p className="project-summary-created-at-text">
            Created at: <span className="font-regular">{project.created_at}</span>
          </p>
          <div className="project-summary-button-container">
            <button type="button" className="b--mat b--affirmative">view queue</button>
            <button type="button" className="b--mat b--affirmative">view job list</button>
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
