import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      project: this.props.project,
    };
  }

  render() {
    const { project } = this.state;

    return (
      <div className="job-header-container">
        <div className="job-header-logo-container">
          <div className="i--icon-logo" />
          <h2 className="font-bold">Foundations</h2>
        </div>
        <div className="job-header-info-container">
          <div>
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">Job List</h1>
            </div>
          </div>
        </div>

        <div className="job-summary-info-container">
          <h2 className="project-summary-name-text font-bold">{ project.name }</h2>
          <p className="project-summary-source-text">Data Source: Unknown</p>
          <p className="project-summary-owner-text font-bold">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="project-summary-created-at-text font-bold">
            Created at: <span>{project.created_at}</span>
          </p>
        </div>
      </div>
    );
  }
}

JobHeader.propTypes = {
  numProjects: PropTypes.number,
  project: PropTypes.object,
};

JobHeader.defaultProps = {
  numProjects: 0,
  project: { owner: 'null', created_at: 'null', name: 'null' },
};

export default JobHeader;
