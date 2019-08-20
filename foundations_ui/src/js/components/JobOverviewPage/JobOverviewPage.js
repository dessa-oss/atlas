import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobOverviewPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.history.location.state.project.name,
      dateCreated: this.props.history.location.state.project.created_at,
      projectOwners: this.props.history.location.state.project.owner,
    };
  }

  render() {
    const { projectName, dateCreated, projectOwners } = this.state;
    return (
      <div className="job-overview-container">
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
            <div className="chart section-container">
              <h3>Recent Jobs</h3>
              <select>
                <option selected="selected">
                Metrics
                </option>
              </select>
              <select>
                <option selected="selected">
                Sort by
                </option>
              </select>
            </div>
            <div className="notes section-container">
              <h3>Notepad</h3>
              <div className="notes-textarea">
                <textarea placeholder="Type something..." />
                <button type="button">Add Note</button>
              </div>
              <div className="notes-blocks">
                <p>Mohammed R. <span>June 25th 2019</span></p>
                <p>This is my message to you</p>
              </div>
            </div>
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
