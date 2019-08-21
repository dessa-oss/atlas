import React from 'react';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import BaseActions from '../../../actions/BaseActions';
import changeIcon from '../../../../scss/jquery/changeIcon';

function SelectJobCell(props) {
  const jobID = props.job.job_id;
  const btnID = `select-job-${jobID}`;

  function handleClick(e) {
    e.stopPropagation();
    // todo functionality here
  }

  return (
    <span
      key={btnID}
      className="select-cell"
    >
      <input type="checkbox" name={btnID} value={jobID} onChange={handleClick} />
    </span>
  );
}

SelectJobCell.propTypes = {
  job: PropTypes.object,
  onSuccessfullDeletion: PropTypes.func,
};

SelectJobCell.defaultProps = {
  job: {},
  onSuccessfullDeletion: () => window.location.reload(),
};

export default SelectJobCell;
