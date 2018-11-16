import React, { Component } from 'react';
import PropTypes from 'prop-types';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cellWidth: this.props.cellWidth,
      value: this.props.value,
      isError: this.props.isError,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ cellWidth: nextProps.cellWidth });
  }

  render() {
    const { cellWidth, value, isError } = this.state;
    const divStyle = {
      width: cellWidth,
    };

    // refactor this and test
    const pClass = isError
      ? ' font-bold error'
      : ' font-bold';

    const divClass = isError
      ? 'input-metric-cell-container error'
      : 'input-metric-cell-container';

    return (
      <div style={divStyle} className={divClass}>
        <p className={pClass}>{value}</p>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  cellWidth: PropTypes.number,
  value: PropTypes.any,
  isError: PropTypes.bool,
};

InputMetricCell.defaultProps = {
  cellWidth: 115,
  value: '',
  isError: false,
};

export default InputMetricCell;
