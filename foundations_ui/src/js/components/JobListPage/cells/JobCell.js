import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.value,
    };
  }

  render() {
    const { value } = this.state;

    return (
      <p className="job-cell">{value}</p>
    );
  }
}

JobCell.propTypes = {
  value: PropTypes.any,
};

JobCell.defaultProps = {
  value: '',
};

export default JobCell;
