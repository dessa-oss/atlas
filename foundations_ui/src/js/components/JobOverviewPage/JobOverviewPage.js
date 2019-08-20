import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobOverviewGraph from './JobOverviewGraph';
import BaseActions from '../../actions/BaseActions';
import Notes from './Notes';

class JobOverviewPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.history.location.state.project.name,
      dateCreated: this.props.history.location.state.project.created_at,
      projectOwners: this.props.history.location.state.project.owner,
      metric: '',
      graphData: [],
    };

    this.getGraphData = this.getGraphData.bind(this);
  }

  componentDidMount() {
    this.getGraphData();
  }

  async getGraphData() {
    const { projectName } = this.state;
    const URL = '/projects/'.concat(projectName).concat('/graph');
    const APIGraphData = await BaseActions.getFromApiary(URL);
    this.setState({ graphData: APIGraphData.data, metric: APIGraphData.metric });
  }

  render() {
    const {
      projectName, dateCreated, projectOwners, metric, graphData,
    } = this.state;

    return (
      <div className="job-overview-container">
        <div className="foundations-header">
          <div className="i--icon-dessa-logo" />
          <div className="header-link-container">
            <a href="/project">Project</a>
            <a href="/documentation">Documentation</a>
            <a href="/support">Support</a>
          </div>
        </div>
        <div className="job-overview-header-container">
          <div>
            <h3>Project Directory</h3>
            <h1 className="font-bold">{projectName}</h1>
          </div>
          <div>
            <p>Date Created: {dateCreated}</p>
            <p>Project Owners: {projectOwners}</p>
          </div>
        </div>
        <div className="job-overview-tabs-tags-container">
          <div>
            <h3>Project Overview</h3>
            <h3>Job Details</h3>
          </div>
          <div>
            <p className="job-overview-tags-text">tags:</p>
            <div className="job-overview-tag">
              <p className="job-overview-tag-name">Finance</p>
            </div>
            <div className="job-overview-tag">
              <p className="job-overview-tag-name">Marketing</p>
            </div>
          </div>
        </div>
        <div className="dashboard-content-container row">
          <section className="chart-and-notes col-md-8">
            <JobOverviewGraph metric={metric} graphData={graphData} />
            <Notes />
          </section>
          <div className="readme section-container col-md-4">
            <h2>README.md</h2>
            <textarea placeholder="Type something...">
            Customer churn and engagement has become one
            of the top issues for most banks.
            It costs significantly more to acquire new customers
            than retain existing ones, and it costs far more to
            re-acquire defected customers. In fact, several empirical
            studies and models have proven that churn remains one of
            the biggest destructors of enterprise value for banks and
            other consumer intensive companies.
            1. Introduction
            We aim to accomplish the following for this study:
            Identify and visualize which factors contribute to customer churn:
            Build a prediction model that will perform the following:
            Classify if a customer is going to churn or not
            </textarea>
          </div>
        </div>
      </div>
    );
  }
}

JobOverviewPage.propTypes = {
  history: PropTypes.object,

};

JobOverviewPage.defaultProps = {
  history: {},
};

export default JobOverviewPage;
