import React from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import ProjectHeader from './ProjectHeader';
import Loading from '../common/Loading';
import { get } from '../../actions/BaseActions';
import ProjectSummary from './ProjectSummary';
import moment from 'moment';

class ProjectPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      projects: [],
      timerId: -1,
    };

    this.reload = this.reload.bind(this);
    this.startTimer = this.startTimer.bind(this);
    this.stopTimer = this.stopTimer.bind(this);
  }

  reload(showAnimation) {
    if (showAnimation === true) {
      this.setState({
        isLoading: true,
      });
    }

    get('projects').then(result => {
      if (result != null) {
        result.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(b.created_at);

          return dateB - dateA;
        });
        this.setState({
          projects: result,
        });
      }
      this.setState({
        isLoading: false,
      });
    }).catch(() => {
      this.setState({
        isLoading: false,
      });
    });
  }

  startTimer() {
    const id = setInterval(() => {
      this.reload(false);
    }, 30000);
    this.setState({
      timerId: id,
    });
  }

  stopTimer() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  componentDidMount() {
    this.reload(true);
    this.startTimer();
  }

  componentWillUnmount() {
    this.stopTimer();
  }

  renderProjects() {
    const { isLoading, projects } = this.state;
    const { selectProject, changePage } = this.props;
    if (isLoading) {
      return <Loading loadingMessage="We are currently loading your projects" />;
    }
    if (projects.length === 0) {
      return <p>No projects available</p>;
    }
    return projects.map(project => {
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
          selectProject={selectProject}
          changePage={changePage}
        />
      );
    });
  }

  render() {
    const { projects } = this.state;
    return (
      <div className="project-page-container">
        <div className="header">
          <Toolbar />
          <ProjectHeader numProjects={projects.length} />
        </div>
        <div className="projects-body-container">{this.renderProjects()}</div>
      </div>
    );
  }
}

ProjectPage.propTypes = {
  selectProject: PropTypes.func,
  changePage: PropTypes.func,
};

ProjectPage.defaultProps = {
  selectProject: () => null,
  changePage: () => null,
};

export default ProjectPage;
