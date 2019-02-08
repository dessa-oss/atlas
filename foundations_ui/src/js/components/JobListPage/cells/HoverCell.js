import React, { Component } from 'react';
import PropTypes from 'prop-types';

class HoverCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: this.props.textToRender,
    };
  }

  render() {
    const { text } = this.state;
    return (
      <div className="job-cell-hover">
        {text}
      </div>
    );
  }
}

HoverCell.propTypes = {
  textToRender: PropTypes.object,
};

HoverCell.defaultProps = {
  textToRender: <p />,
};

export default HoverCell;
