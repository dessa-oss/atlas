import React, { Component } from 'react';
import PropTypes from 'prop-types';

class CancelJobCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
    };
  }

  render() {
    const { job } = this.state;

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
}

CancelJobCell.propTypes = {
  job: PropTypes.object,
};

CancelJobCell.defaultProps = {
  job: {},
};

export default CancelJobCell;
