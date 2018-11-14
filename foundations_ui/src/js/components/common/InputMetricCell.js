import React, { Component } from 'react';
import PropTypes from 'prop-types';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cellWidth: this.props.cellWidth,
      value: this.props.value,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ cellWidth: nextProps.cellWidth });
  }

  render() {
    const { cellWidth, value } = this.state;
    const divStyle = {
      width: cellWidth,
    };

    return (
      <div style={divStyle} className="input-metric-cell-container">
        <p className="header-4 font-bold">{value}</p>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  cellWidth: PropTypes.number,
  value: PropTypes.any,
};

InputMetricCell.defaultProps = {
  cellWidth: 115,
  value: '',
};

export default InputMetricCell;
