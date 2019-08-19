import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';

const ProjectSummary = (props) => {
  const packageClick = () => {
    const { history, project } = props;

    history.push(
      `/projects/${project.name}/job_overview`,
      {
        project,
      },
    );
  };

  const { project } = props;


  return (
    <div
      className="project-summary-container elevation-1"
      onClick={packageClick}
      role="button"
      tabIndex={0}
      onKeyPress={packageClick}
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
};

ProjectSummary.propTypes = {
  project: PropTypes.object,
  history: PropTypes.object,
};

ProjectSummary.defaultProps = {
  project: {},
  history: {},
};

export default withRouter(ProjectSummary);
