import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cellWidths: this.props.cellWidths,
      isError: this.props.isError,
      job: this.props.job,
    };
  }

  render() {
    const { job, cellWidths, isError } = this.state;

    const cells = CommonActions.getInputMetricCells(job, cellWidths, isError);

    return (
      <div className="job-table-row">
        {cells}
      </div>
    );
  }
}

InputMetricRow.propTypes = {
  job: PropTypes.object,
  cellWidths: PropTypes.array,
  isError: PropTypes.bool,
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
  isError: false,
};

export default InputMetricRow;
