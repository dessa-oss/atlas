import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

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

    const pClass = CommonActions.getInputMetricCellPClass(isError);
    const divClass = CommonActions.getInputMetricCellDivClass(isError);

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
