import React, { Component } from 'react';
import PropTypes from 'prop-types';
import BaseActions from '../../../actions/BaseActions';

function CancelJobCell(props) {
  function handleClick() {
    let uri = `projects/dummy_project_name/job_listing/${props.job.job_id}`;

    if (window.confirm(`Are you sure you want to cancel job ${props.job.job_id}?`)) {
      BaseActions.deleteBetaFromAPI(uri).then(() => window.location.reload());
    }
  }

  return (
    <div
      className="job-cell cancel-cell"
      style={{ cursor: 'pointer', width: '1em' }}
    >
      <button type="button" className="job-cell i--icon-delete" onClick={handleClick} onKeyDown={handleClick} />
    </div>
  );
}

CancelJobCell.propTypes = {
  job: PropTypes.object,
};

CancelJobCell.defaultProps = {
  job: {},
};

export default CancelJobCell;
