import React, { Component } from 'react';
import PropTypes from 'prop-types';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cellWidth: this.props.cellWidth,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ cellWidth: nextProps.cellWidth });
  }

  render() {
    const { cellWidth } = this.state;
    const divStyle = {
      width: cellWidth,
    };

    return (
      <div style={divStyle} className="input-metric-cell-container">
        <p>value</p>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  cellWidth: PropTypes.number,
};

InputMetricCell.defaultProps = {
  cellWidth: 115,
};

export default InputMetricCell;
