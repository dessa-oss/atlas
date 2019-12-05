import React from 'react';
import PropTypes from 'prop-types';

function SelectJobCell(props) {
  const jobID = props.job.job_id;
  const btnID = `select-job-${jobID}`;
  const isSelectedJob = props.isSelectedJob;

  function handleClick(e) {
    e.stopPropagation();
    props.selectJob(e.target.value);
  }

  return (
    <span
      key={btnID}
      className="select-cell"
    >
      <input type="checkbox" name={btnID} value={jobID} onChange={handleClick} checked={isSelectedJob} />
    </span>
  );
}

SelectJobCell.propTypes = {
  job: PropTypes.object,
  onSuccessfullDeletion: PropTypes.func,
  selectJob: PropTypes.func,
  isSelectedJob: PropTypes.bool,
};

SelectJobCell.defaultProps = {
  job: {},
  onSuccessfullDeletion: () => window.location.reload(),
  selectJob: () => {},
  isSelectedJob: false,
};

export default SelectJobCell;
