import { CopyToClipboard } from 'react-copy-to-clipboard';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';

import 'react-toastify/dist/ReactToastify.css';

class JobIDCell extends Component {
  constructor(props) {
    super(props);

    this.state = {
      jobID: this.props.jobID,
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  notifiedCopy(e) {
    e.stopPropagation();
    toast.info('Job ID successfully copied', {
      autoClose: 1500,
      draggable: false,
    });
  }

  render() {
    const {
      jobID, isError, rowNumber,
    } = this.state;

    const aClass = isError
      ? `job-id-cell error row-${rowNumber}`
      : `job-id-cell row-${rowNumber}`;

    // const href = '/'.concat(jobID);
    return (
      <span>
        <span className={aClass}>{jobID}</span>
        <CopyToClipboard text={jobID}>
          <span
            onClick={this.notifiedCopy}
            className="i--icon-copy"
            role="presentation"
          />
        </CopyToClipboard>
      </span>
    );
  }
}

JobIDCell.propTypes = {
  jobID: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

JobIDCell.defaultProps = {
  jobID: '',
  isError: false,
  rowNumber: 0,
};

export default JobIDCell;
