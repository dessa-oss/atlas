import React, { Component } from 'react';
import PropTypes from 'prop-types';

function CancelJobCell(props) {
  function handleClick() {
  }

  return (
    <h2
      className="job-cell"
      type="button"
      onClick={handleClick}
      onKeyDown={handleClick}
      style={{ cursor: 'pointer', width: '1em' }}
    >🗑
    </h2>
  );
}

CancelJobCell.propTypes = {
  job: PropTypes.object,
};

CancelJobCell.defaultProps = {
  job: {},
};

export default CancelJobCell;
