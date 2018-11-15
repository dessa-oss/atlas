import React, { Component } from 'react';
import PropTypes from 'prop-types';

class UserCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
      isError: this.props.isError,
    };
  }

  render() {
    const { user, isError } = this.state;

    const pClass = isError
      ? 'job-cell user-cell font-regular error'
      : 'job-cell user-cell font-regular';
    return (
      <p className={pClass}>{user}</p>
    );
  }
}

UserCell.propTypes = {
  user: PropTypes.string,
  isError: PropTypes.bool,
};

UserCell.defaultProps = {
  user: '',
  isError: false,
};

export default UserCell;
