import React, { Component } from 'react';
import PropTypes from 'prop-types';

class HoverCell extends Component {
  render() {
    const { textToRender, onMouseLeave } = this.props;
    return (
      <div onMouseLeave={onMouseLeave} className="job-cell-hover" data-class="hover-cell">
        {textToRender}
      </div>
    );
  }
}

HoverCell.propTypes = {
  textToRender: PropTypes.object,
  onMouseLeave: PropTypes.func,
};

HoverCell.defaultProps = {
  textToRender: <p />,
  onMouseLeave: () => {},
};

export default HoverCell;
