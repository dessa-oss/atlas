import React, { Component } from 'react';
import JobColumnHeader from './JobColumnHeader';

class JobTableHeader extends Component {
  render() {
    return (
      <div className="job-list-container">
        <JobColumnHeader title="Start Time" />
        <JobColumnHeader title="Status" isStatus={1} />
        <JobColumnHeader title="Job ID" />
        <JobColumnHeader title="Duration" />
        <JobColumnHeader title="User" />
      </div>
    );
  }
}

export default JobTableHeader;
