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
      jobID: this.props.jobID,
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
      jobID: nextProps.jobID,
    });
  }

  getDisplayText(value) {
    if (value.key !== undefined) { // we know its a react element
      if (value.key === null) { // the react element does not have a value set to display
        return '';
      }
      return value.key;
    }
    return value; // typical content
  }

  isContentOverMaxLength(displayText) {
    const maxCellCharacterLength = 13;
    return displayText.toString().length > maxCellCharacterLength || displayText.length > maxCellCharacterLength;
  }

  render() {
    const {
      value, isError, cellType, rowNumber, expand, hoverable, jobID,
    } = this.state;

    const pClass = CommonActions.getInputMetricCellPClass(isError, cellType);
    const divClass = CommonActions.getInputMetricCellDivClass(isError, rowNumber, jobID);
    let hover;

    if (expand) {
      const displayText = this.getDisplayText(value);
      const overMaxLength = this.isContentOverMaxLength(displayText);

      if (overMaxLength && hoverable) {
        hover = <HoverCell textToRender={displayText} />;
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
  jobID: PropTypes.string,
};

InputMetricCell.defaultProps = {
  value: '',
  isError: false,
  cellType: '',
  rowNumber: 0,
  hoverable: true,
  jobID: '',
};

export default InputMetricCell;
