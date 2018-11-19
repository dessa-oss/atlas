import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
      cellWidths: this.props.cellWidths,
    };
  }

  render() {
    const { job, cellWidths } = this.state;

    const cells = CommonActions.getInputMetricCells(job, cellWidths);

    return (
      <div className="input-metric-rows-container">
        {cells}
      </div>
    );
  }
}

InputMetricRow.propTypes = {
  job: PropTypes.object,
  cellWidths: PropTypes.array,
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
};

export default InputMetricRow;
