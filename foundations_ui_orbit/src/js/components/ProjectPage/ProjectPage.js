import React, { Component } from "react";
import PropTypes from "prop-types";
import Toolbar from "../common/Toolbar";
import ProjectHeader from "./ProjectHeader";
import Loading from "../common/Loading";
import BaseActions from "../../actions/BaseActions";
import ProjectSummary from "./ProjectSummary";
import moment from "moment";

class ProjectPage extends Component {
  constructor(props) {
    super(props);
    this.getAllProjects = this.getAllProjects.bind(this);
    this.state = {
      isLoaded: false,
      projects: this.props.projects,
      isMount: false,
      selectProject: this.props.selectProject,
      changePage: this.props.changePage
    };
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    this.getAllProjects();
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
  }

  async getAllProjects() {
    const projects = await BaseActions.get("projects");

    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (projects != null) {
        projects.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(a.created_at);

          return dateB - dateA;
        });
        this.setState({ projects: projects, isLoaded: true });
      } else {
        this.setState({ projects: [], isLoaded: true });
      }
    }
  }

  render() {
    const { isLoaded, projects, selectProject, changePage } = this.state;
    let projectList = [];
    if (isLoaded) {
      if (projects.length === 0) {
        projectList = <p>No projects available</p>;
      } else {
        projects.forEach(project => {
          const key = project.name.concat("-").concat(project.created_at);
          const formattedDate = moment(project.created_at)
            .format("YYYY-MM-DD HH:mm")
            .toString();
          project.created_at = formattedDate;
          projectList.push(
            <ProjectSummary
              key={key}
              project={project}
              selectProject={selectProject}
              changePage={changePage}
            />
          );
        });
      }
    } else {
      projectList = (
        <Loading loadingMessage="We are currently loading your projects" />
      );
    }

    return (
      <div className="project-page-container">
        <div className="header">
          <Toolbar />
          <ProjectHeader numProjects={projects.length} />
        </div>
        <div className="projects-body-container">{projectList}</div>
      </div>
    );
  }
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
