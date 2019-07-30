import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import HoverCell from '../JobListPage/cells/HoverCell';

class InputMetricCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.state = {
      value: this.props.value,
      isError: this.props.isError,
      cellType: this.props.cellType,
      rowNumber: this.props.rowNumber,
      hoverable: this.props.hoverable,
    };
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      value: nextProps.value,
      cellType: nextProps.cellType,
      rowNumber: nextProps.rowNumber,
      isError: nextProps.isError,
      hoverable: nextProps.hoverable,
    });
    // if (nextProps.rowNumber !== this.props.rowNumber) {
    //   this.setState({
    //     value: nextProps.value,
    //     cellType: nextProps.cellType,
    //     rowNumber: nextProps.rowNumber,
    //     isError: nextProps.isError,
    //     hoverable: nextProps.hoverable,
    //   });
    // }
  }

  render() {
    const {
      value, isError, cellType, rowNumber, expand, hoverable,
    } = this.state;

    const pClass = CommonActions.getInputMetricCellPClass(isError, cellType);
    const divClass = CommonActions.getInputMetricCellDivClass(isError, rowNumber);

    let hover;

    if (expand) {
      const maxCellCharacterLength = 13;
      const overMaxLength = value.toString().length > maxCellCharacterLength || value.length > maxCellCharacterLength;
      if (overMaxLength && hoverable) {
        hover = <HoverCell textToRender={value} />;
      }
    }

    return (
      <div className={divClass}>
        <p
          className={pClass}
          onMouseEnter={() => this.toggleExpand(true)}
          onMouseLeave={() => this.toggleExpand(false)}
        >
          {value}
        </p>
        <div>
          {hover}
        </div>
      </div>
    );
  }
}

InputMetricCell.propTypes = {
  value: PropTypes.any,
  isError: PropTypes.bool,
  cellType: PropTypes.string,
  rowNumber: PropTypes.number,
  hoverable: PropTypes.bool,
};

InputMetricCell.defaultProps = {
  value: '',
  isError: false,
  cellType: '',
  rowNumber: 0,
  hoverable: true,
};

export default InputMetricCell;
