import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';

const ProjectSummary = (props) => {
  const packageClick = () => {
    const { history, project } = props;

    history.push(
      `/projects/${project.name}/overview`,
      {
        project,
      },
    );
  };

  const { project } = props;


  return (
    <div
      className="project-summary-container"
      onClick={packageClick}
      role="button"
      tabIndex={0}
      onKeyPress={packageClick}
    >
      <div className="project-summary-info-container">
        <h2 className="font-bold">{project.name}</h2>
        {/* <p>Data Source: Unknown</p> */}
        <p className="font-bold">
          Project owner: <span>{project.owner}</span>
        </p>
        <p className="font-bold">
          Created at: <span>{project.created_at}</span>
        </p>
        <div className="project-summary-button-container" />
      </div>
      <div className="project-summary-tags-container">
        <p>tags</p>
        <span>finance</span>
        <span>marketing</span>
      </div>
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
