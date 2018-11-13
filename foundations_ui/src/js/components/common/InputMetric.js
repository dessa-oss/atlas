import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import JobColumnHeader from './JobColumnHeader';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.state = {
      header: this.props.header,
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
    };
  }

  render() {
    const { header, hiddenInputParams, allInputParams } = this.state;

    let inputParams = null;
    if (allInputParams.length > 0) {
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(<JobColumnHeader key={key} title={input} className="inline-block" containerClass="input-metric-column-header" />);
      });
    }

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
        <div className="input-metric-column-header-container">
          {inputParams}
        </div>
      </div>
    );
  }
}

InputMetric.propTypes = {
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
};


export default InputMetric;
