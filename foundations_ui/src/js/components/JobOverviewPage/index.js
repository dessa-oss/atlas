import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Header from './Header';
import ProjectOverview from './ProjectOverview';
import JobDetails from './JobDetails';
import CommonHeader from '../common/CommonHeader';

class JobOverviewPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      tab: 'overview',
    };

    this.onClickProjectOverview = this.onClickProjectOverview.bind(this);
    this.onClickJobDetails = this.onClickJobDetails.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  onClickProjectOverview() {
    this.setState({
      tab: 'overview',
    });
  }

  onClickJobDetails() {
    this.setState({
      tab: 'details',
    });
  }

  onKeyDown() {}

  render() {
    const { tab } = this.state;

    return (
      <div>
        <CommonHeader {...this.props} />
        <div className="job-overview-container">
          <Header {...this.props} />
          <div className="job-overview-tabs-tags-container">
            <div>
              <h3 onClick={this.onClickProjectOverview} onKeyDown={this.onKeyDown}>Project Overview</h3>
              <h3 onClick={this.onClickJobDetails} onKeyDown={this.onKeyDown}>Job Details</h3>
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
          {tab === 'overview' && <ProjectOverview {...this.props} />}
          {tab === 'details' && <JobDetails {...this.props} />}
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
