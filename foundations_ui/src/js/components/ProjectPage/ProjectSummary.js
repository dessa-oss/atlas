import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import ProjectActions from '../../actions/ProjectActions';

class ProjectSummary extends Component {
  constructor(props) {
    super(props);
    this.viewClick = this.viewClick.bind(this);
    this.state = {
      project: this.props.project,
    };
  }

  viewClick() {
    this.setState({ redirect: true });
  }

  render() {
    const { project } = this.state;
    if (this.state.redirect) {
      const jobListingPath = `/projects/${project.name}/job_listing`;
      return ProjectActions.redirect(jobListingPath);
    }
    return (
      <div className="project-summary-container elevation-1">
        <div className="project-summary-info-container">
          <h2 className="font-bold">{project.name}</h2>
          <p>Data Source: raw_mnist</p>
          <p className="font-bold">
            Project owner: <span>Trial{project.owner}</span>
          </p>
          <p className="font-bold">
            Created at: <span>2005-10-30 T 10:45 UTC{project.created_at}</span>
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
};

ProjectSummary.defaultProps = {
  project: {},
};

export default ProjectSummary;
