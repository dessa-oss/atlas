import React, { Component } from "react";
import PropTypes from "prop-types";
import Toolbar from "../common/Toolbar";
import ProjectHeader from "./ProjectHeader";
import Loading from "../common/Loading";
import BaseActions from "../../actions/BaseActions";
import ProjectSummary from "./ProjectSummary";
import moment from "moment";

const ProjectPage = props => {

  const [isLoading, setIsLoading] = React.useState(false);
  const [projects, setProjects] = React.useState([]);

  const reload = () => {
    setIsLoading(true);

    BaseActions.get("projects").then((result) => {
      if (result != null) {
        result.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(a.created_at);

          return dateB - dateA;
        });
        setProjects(result);
      }
      setIsLoading(false);
    }).catch((error) => {
      setIsLoading(false);
    });
  }

  React.useEffect(() => {
    reload()
  }, [])

  const renderProjects = () => {
    if (isLoading) {
      return <Loading loadingMessage="We are currently loading your projects" />
    } else {
      if (projects.length === 0) {
        return <p>No projects available</p>;
      } else {
        return projects.map(project => {
          const key = project.name.concat("-").concat(project.created_at);
          const formattedDate = moment(project.created_at)
            .format("YYYY-MM-DD HH:mm")
            .toString();
          project.created_at = formattedDate;
          return (
            <ProjectSummary
              key={key}
              project={project}
              selectProject={props.selectProject}
              changePage={props.changePage}
            />
          );
        });
      } 
    }
  }

  return (
    <div className="project-page-container">
      <div className="header">
        <Toolbar />
        <ProjectHeader numProjects={projects.length} />
      </div>
      <div className="projects-body-container">{renderProjects()}</div>
    </div>
    );
  }


ProjectPage.propTypes = {
  isMount: PropTypes.bool,
  isLoaded: PropTypes.bool,
  projects: PropTypes.array,
  selectProject: PropTypes.func,
  changePage: PropTypes.func
};

ProjectPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  projects: [],
  selectProject: () => null,
  changePage: () => null
};

export default ProjectPage;
