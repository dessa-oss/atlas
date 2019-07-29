import { CopyToClipboard } from 'react-copy-to-clipboard';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import HoverCell from './HoverCell';
import 'react-toastify/dist/ReactToastify.css';

class JobIDCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.state = {
      jobID: this.props.jobID,
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  notifiedCopy() {
    toast.info('Job ID successfully copied', {
      autoClose: 1500,
      draggable: false,
    });
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  render() {
    const {
      jobID, isError, rowNumber, expand,
    } = this.state;

    const jobIdFormatted = <p>{jobID}</p>;

    let hover;

    if (expand) {
      hover = <HoverCell textToRender={jobIdFormatted} />;
    }

    const aClass = isError
      ? `job-cell job-id-cell error row-${rowNumber}`
      : `job-cell job-id-cell row-${rowNumber}`;

    const href = '/'.concat(jobID);
    return (
      <div
        className={aClass}
        onMouseEnter={() => this.toggleExpand(true)}
        onMouseLeave={() => this.toggleExpand(false)}
      >
        {jobIdFormatted}
        <CopyToClipboard text={jobID}>
          <div
            onClick={() => this.notifiedCopy()}
            className="i--icon-copy"
            role="presentation"
          />
        </CopyToClipboard>
        <ToastContainer />
        <div>
          {hover}
        </div>
      </div>
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
