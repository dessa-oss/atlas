import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Tooltip extends Component {
  constructor(props) {
    super(props);
    this.state = {
      message: this.props.message,
    };
  }

  render() {
    const { message } = this.state;
    return (
      <span className="tooltip">{message}</span>
    );
  }
}

Tooltip.propTypes = {
  message: PropTypes.string,
};

Tooltip.defaultProps = {
  message: '',
};

export default Tooltip;
