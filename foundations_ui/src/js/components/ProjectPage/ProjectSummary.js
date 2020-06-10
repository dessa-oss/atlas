import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import CommonActions from '../../actions/CommonActions';

const ProjectSummary = props => {
  const packageClick = () => {
    const { history, project } = props;

    history.push(
      `/projects/${project.name}/job_listing`,
      {
        project: project,
      },
    );
  };

  const { project } = props;

  return (
    <div
      className="project-summary-container"
      data-class="project-summary"
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
        <p className="font-bold">
          Created at: <span>{CommonActions.formatDate(project.created_at)}</span>
        </p>
        <div className="project-summary-button-container" />
      </div>
      <p>tags</p>
      <div className="project-summary-tags-container">
        {project.tags.map(tag => {
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
