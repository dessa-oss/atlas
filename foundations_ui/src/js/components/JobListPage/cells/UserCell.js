import React, { Component } from 'react';
import PropTypes from 'prop-types';

class UserCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
    };
  }

  render() {
    const { user } = this.state;

    return (
      <p className="job-cell user-cell font-regular">{user}</p>
    );
  }
}

UserCell.propTypes = {
  user: PropTypes.string,
};

UserCell.defaultProps = {
  user: '',
};

export default UserCell;
