import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import HoverCell from '../JobListPage/cells/HoverCell';

const ProjectSummary = (props) => {
  const [showAllTags, setShowAllTags] = React.useState(false);

  const packageClick = () => {
    const { history, project } = props;

    history.push(
      `/projects/${project.name}/overview`,
      {
        project,
      },
    );
  };

  const onClickShowTags = () => {
    const { project } = props;
    const value = !showAllTags;
    setShowAllTags(value);
  };

  const onMouseLeave = () => {
    setShowAllTags(false);
  };

  const { project } = props;

  let expandedTagSpans = [];
  project.tags.forEach((tag) => {
    expandedTagSpans.push(<span key={'tag-'.concat(tag)}>{tag}</span>);
  });

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
          Project owner: <span>CE User</span>
        </p>
        <p className="font-bold">
          Created at: <span>{project.created_at}</span>
        </p>
        <div className="project-summary-button-container" />
      </div>
      <div className="project-summary-tags-container">
        <p>tags</p>
        {project.tags.slice(0, 10).map((tag) => {
          return <span key={tag}>{tag}</span>;
        })}
        {project.tags.length > 10
          && (
            <span
              className="span-more"
              role="presentation"
              onClick={onClickShowTags}
              onKeyDown={() => {}}
            >
                ...
            </span>
          )
        }
        {showAllTags && <HoverCell onMouseLeave={onMouseLeave} textToRender={expandedTagSpans} />}
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
