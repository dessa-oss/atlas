import React, { Component } from 'react';
import PropTypes from 'prop-types';

class UserCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.rowNumber !== this.props.rowNumber) {
      this.setState({
        rowNumber: nextProps.rowNumber,
        isError: nextProps.isError,
        user: nextProps.user,
      });
    }
  }

  render() {
    const { user, isError, rowNumber } = this.state;

    const pClass = isError
      ? `job-cell user-cell error row-${rowNumber}`
      : `job-cell user-cell row-${rowNumber}`;
    return (
      <p className={pClass}>{user}</p>
    );
  }
}

UserCell.propTypes = {
  user: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

UserCell.defaultProps = {
  user: '',
  isError: false,
  rowNumber: 0,
};

export default UserCell;
