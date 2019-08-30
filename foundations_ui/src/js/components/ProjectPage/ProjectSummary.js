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
    >
      <div className="project-summary-info-container">
        <h2
          onClick={packageClick}
          // eslint-disable-next-line jsx-a11y/no-noninteractive-element-to-interactive-role
          role="button"
          tabIndex={0}
          onKeyPress={packageClick}
          className="font-bold"
        >
          {project.name}
        </h2>
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
        {project.tags.slice(0, 5).map((tag) => {
          return <span key={tag}>{tag}</span>;
        })}
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
