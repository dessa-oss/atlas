import React from 'react';
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import BaseActions from '../../../actions/BaseActions';
import changeIcon from '../../../../scss/jquery/changeIcon';

function CancelJobCell(props) {
  const jobID = props.job.job_id;
  const btnID = `del-btn-${jobID}`;

  function notifyDeleted() {
    toast.success('Job successfully deleted', {
      autoClose: 3000,
      draggable: false,
    });
  }

  function notifyFailed() {
    toast.error(`Failed to delete job ${jobID}`, {
      autoClose: 1500,
      draggable: false,
    });
  }

  function handleClick(e) {
    e.stopPropagation();

    const uri = `projects/dummy_project_name/job_listing/${jobID}`;
    const message = `Are you sure you want to cancel job ${jobID}?`;
    if (window.confirm(message)) {
      changeIcon.changeIconByAccessorAndDisabled(`#${btnID}`, 'i--icon-loading');

      BaseActions.deleteBetaFromAPI(uri).then(() => {
        notifyDeleted();
        props.onSuccessfullDeletion();
      }).catch(() => {
        changeIcon.changeIconByAccessorAndEnabled(`#${btnID}`, 'i--icon-delete');
        notifyFailed();
      });
    }
  }

  return (
    <span
      className="cancel-cell"
      style={{ cursor: 'pointer', width: '1em' }}
    >
      <button
        type="button"
        id={btnID}
        className="i--icon-delete"
        onClick={handleClick}
        onKeyDown={handleClick}
      />
      <ToastContainer />
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
