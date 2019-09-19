import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import Header from './Header';
import ProjectOverview from './ProjectOverview';
import JobDetails from './JobDetails';
import CommonHeader from '../common/CommonHeader';
import TagContainer from './TagContainer';
import BaseActions from '../../actions/BaseActions';
import ErrorPage from '../common/ErrorPage';
import CommonFooter from '../common/CommonFooter';

class JobOverviewPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      tab: 'details',
      tags: [],
      showErrorPage: false,
    };

    this.onClickProjectOverview = this.onClickProjectOverview.bind(this);
    this.onClickJobDetails = this.onClickJobDetails.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  async reload() {
    const { location } = this.props;
    if (!location.state || !location.state.project || location.state.project === {}) {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.get('projects');
      const selectedProject = fetchedProjects.filter(item => item.name === projectName);
      if (selectedProject.length === 0 || selectedProject === undefined) {
        this.setState({
          showErrorPage: true,
        });
      } else {
        this.setState({
          tags: selectedProject.tags,
        });
      }
    }
  }

  componentDidMount() {
    this.reload();
  }

  async onClickProjectOverview() {
    const { history, location } = this.props;
    let selectedProject = {};

    if (location.state.project && location.state.project !== {}) {
      selectedProject = location.state.project;
    } else {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.get('projects');
      selectedProject = fetchedProjects.filter(item => item.name === projectName);
    }
    history.push(
      `/projects/${selectedProject.name}/overview`,
      {
        project: selectedProject,
      },
    );
  }

  async onClickJobDetails() {
    const { history, location } = this.props;
    let selectedProject = {};

    if (location.state.project && location.state.project !== {}) {
      selectedProject = location.state.project;
    } else {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.get('projects');
      selectedProject = fetchedProjects.filter(item => item.name === projectName);
    }
    history.push(
      `/projects/${selectedProject.name}/job_listing`,
      {
        project: selectedProject,
      },
    );
  }

  onKeyDown() {}

  render() {
    const { tab, tags, showErrorPage } = this.state;
    const { location } = this.props;

    if (showErrorPage === true) {
      return (
        <div>
          <CommonHeader {...this.props} />
          <ErrorPage {...this.props} />
        </div>
      );
    }

    return (
      <div>
        <CommonHeader {...this.props} />
        <div className="job-overview-container">
          <Header {...this.props} />
          <div className="job-overview-tabs-tags-container">
            <div>
              <h3
                className={tab === 'overview' ? 'active' : ''}
                onClick={this.onClickProjectOverview}
                onKeyDown={this.onKeyDown}
              >
                Project Overview
              </h3>
              <h3
                className={tab === 'details' ? 'active' : ''}
                onClick={this.onClickJobDetails}
                onKeyDown={this.onKeyDown}
              >
                Job Details
              </h3>
            </div>
            <TagContainer tags={tags} />
          </div>
          {tab === 'overview' && <ProjectOverview {...this.props} />}
          {tab === 'details' && <JobDetails {...this.props} />}
        </div>
        <CommonFooter />
      </div>
    );
  }
}

JobOverviewPage.propTypes = {
  history: PropTypes.object,
  location: PropTypes.object,
  match: PropTypes.object,
};

JobOverviewPage.defaultProps = {
  history: {},
  location: { state: {} },
  match: { params: {} },
};

export default withRouter(JobOverviewPage);
