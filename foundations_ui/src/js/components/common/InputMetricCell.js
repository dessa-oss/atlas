import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.value,
      isError: this.props.isError,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ value: nextProps.value });
  }

  render() {
    const { value, isError } = this.state;

    const pClass = CommonActions.getInputMetricCellPClass(isError);
    const divClass = CommonActions.getInputMetricCellDivClass(isError);

    return (
      <div className={divClass}>
        <p className={pClass}>{value}</p>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  value: PropTypes.any,
  isError: PropTypes.bool,
};

InputMetricCell.defaultProps = {
  value: '',
  isError: false,
};

export default InputMetricCell;
