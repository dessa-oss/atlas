import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import BaseActions from '../../../actions/BaseActions';

function CancelJobCell(props) {
  function notifyDeleted() {
    toast.success('Job successfully deleted', {
      autoClose: 3000,
      draggable: false,
    });
  }

  function notifyFailed() {
    toast.error(`Failed to delete job ${props.job.job_id}`, {
      autoClose: 1500,
      draggable: false,
    });
  }

  function handleClick(e) {
    e.stopPropagation();
    let uri = `projects/dummy_project_name/job_listing/${props.job.job_id}`;
    if (window.confirm(`Are you sure you want to cancel job ${props.job.job_id}?`)) {
      BaseActions.deleteBetaFromAPI(uri).then(() => {
        props.onSuccessfullDeletion();
        notifyDeleted();
      }).catch(() => notifyFailed());
    }
  }

  return (
    <span
      className="cancel-cell"
      style={{ cursor: 'pointer', width: '1em' }}
    >
      <button type="button" className="i--icon-delete" onClick={handleClick} onKeyDown={handleClick} />
    </span>
  );
}

CancelJobCell.propTypes = {
  job: PropTypes.object,
  onSuccessfullDeletion: PropTypes.func,
};

CancelJobCell.defaultProps = {
  job: {},
  onSuccessfullDeletion: () => window.location.reload(),
};

export default CancelJobCell;
