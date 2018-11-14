import React, { Component } from 'react';
import JobColumnHeader from './JobColumnHeader';

class JobTableHeader extends Component {
  render() {
    return (
      <div className="job-list-container">
        <JobColumnHeader title="Start Time" className="start-time-offset" />
        <JobColumnHeader title="Status" isStatus={1} className="status-offset" />
        <JobColumnHeader title="Job ID" className="job-id-offset" />
        <JobColumnHeader title="Duration" className="duration-offset" />
        <JobColumnHeader title="User" className="user-offset" />
      </div>
    );
  }
}

export default JobTableHeader;
