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
