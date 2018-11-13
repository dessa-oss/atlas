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
    };
  }

  render() {
    const { header, hiddenInputParams } = this.state;

    let inputParams = null;
    if (hiddenInputParams.length > 0) {
      inputParams = [];
      hiddenInputParams.forEach((input) => {
        const key = input.name;
        inputParams.push(<JobColumnHeader key={key} job={input.name} />);
      });
    }

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
        {inputParams}
      </div>
    );
  }
}

InputMetric.propTypes = {
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
};


export default InputMetric;
