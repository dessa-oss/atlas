import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numProjects: this.props.numProjects,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ numProjects: nextProps.numProjects });
  }

  render() {
    const { numProjects } = this.state;

    return (
      <div className="job-header-container">
        <div className="job-header-logo-container">
          <div className="i--icon-logo" />
          <h2 className="font-bold">Foundations</h2>
        </div>
        <div className="job-header-info-container">
          <div>
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">Job List</h1>
            </div>
          </div>
        </div>

        <div className="job-summary-info-container">
          <h2 className="project-summary-name-text font-bold">Name</h2>
          <p className="project-summary-source-text">Data Source: Unknown</p>
          <p className="project-summary-owner-text font-bold">
            Project owner: <span>Owner</span>
          </p>
          <p className="project-summary-created-at-text font-bold">
            Created at: <span>12:00</span>
          </p>
        </div>
      </div>
    );
  }
}

JobHeader.propTypes = {
  numProjects: PropTypes.number,
};

JobHeader.defaultProps = {
  numProjects: 0,
};

export default JobHeader;
