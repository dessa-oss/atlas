import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Toolbar from '../common/Toolbar';
import ProjectHeader from './ProjectHeader';
import Loading from '../common/Loading';
import BaseActions from '../../actions/BaseActions';
import ProjectSummary from './ProjectSummary';

const ProjectPage = (props) => {
  const [isLoading, setIsLoading] = React.useState(false);
  const [projects, setProjects] = React.useState([]);

  const reload = () => {
    setIsLoading(true);

    BaseActions.get('projects').then((result) => {
      if (result != null) {
        result.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(b.created_at);

          return dateB - dateA;
        });
        setProjects(result);
      }
      setIsLoading(false);
    }).catch(() => {
      setIsLoading(false);
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const renderProjects = () => {
    if (isLoading) {
      return <Loading loadingMessage="We are currently loading your projects" />;
    }
    if (projects.length === 0) {
      return <p>No projects available</p>;
    }
    return projects.map((project) => {
      const newProject = project;
      const key = newProject.name.concat('-').concat(newProject.created_at);
      const formattedDate = moment(newProject.created_at)
        .format('YYYY-MM-DD HH:mm')
        .toString();
      newProject.created_at = formattedDate;
      return (
        <ProjectSummary
          key={key}
          project={newProject}
          selectProject={props.selectProject}
          changePage={props.changePage}
        />
      );
    });
  };

  return (
    <div className="project-page-container">
      <div className="header">
        <Toolbar />
        <ProjectHeader numProjects={projects.length} />
      </div>
      <div className="projects-body-container">{renderProjects()}</div>
    </div>
  );
};


ProjectPage.propTypes = {
  selectProject: PropTypes.func,
  changePage: PropTypes.func,
};

ProjectPage.defaultProps = {
  selectProject: () => null,
  changePage: () => null,
};

export default ProjectPage;
