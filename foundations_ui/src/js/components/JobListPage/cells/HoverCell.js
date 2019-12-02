import React, { Component } from 'react';
import PropTypes from 'prop-types';

class HoverCell extends Component {
  render() {
    const { textToRender, onMouseLeave, dataClass } = this.props;
    return (
      <div onMouseLeave={onMouseLeave} className="job-cell-hover" data-class={dataClass}>
        {textToRender}
      </div>
    );
  }
}

HoverCell.propTypes = {
  textToRender: PropTypes.object,
  onMouseLeave: PropTypes.func,
  dataClass: PropTypes.string,
};

HoverCell.defaultProps = {
  textToRender: <p />,
  onMouseLeave: () => {},
  dataClass: '',
};

export default HoverCell;
