import React, { Component } from 'react';
import PropTypes from 'prop-types';

class TrainingDateRow extends Component {
  constructor(props) {
    super(props);
    this.clickX = this.clickX.bind(this);
    this.state = {
      date: this.props.date,
      isAddRow: this.props.isAddRow,
      removeDate: this.props.removeDate,
    };
  }

  clickX(){
    const { removeDate, date } = this.state;
    removeDate(date);
  }

  render() {
    const { date, isAddRow } = this.state;

    let closeButton = null;
    if (!isAddRow) {
      closeButton = <div className="close-button" onClick={this.clickX} />
    }

    return (
      <div className="training-row-container">
        <p className="training-row">{date}</p>
        {closeButton}
      </div>
    );
  }
}
TrainingDateRow.propTypes = {
  date: PropTypes.string,
  isAddRow: PropTypes.bool,
  removeDate: PropTypes.func,
};

TrainingDateRow.defaultProps = {
  date: "",
  isAddRow: false,
  removeDate: () => {},
};
export default TrainingDateRow;
