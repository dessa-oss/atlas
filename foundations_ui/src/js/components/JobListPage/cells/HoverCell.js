import React, { Component } from 'react';
import PropTypes from 'prop-types';

class HoverCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: this.props.textToRender,
      onMouseLeave: this.props.onMouseLeave,
    };
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.text !== this.props.text) {
      this.setState({
        text: nextProps.text,
      });
    }
  }

  render() {
    const { text, onMouseLeave } = this.state;
    return (
      <div onMouseLeave={onMouseLeave} className="job-cell-hover">
        {text}
      </div>
    );
  }
}

HoverCell.propTypes = {
  textToRender: PropTypes.object,
  text: PropTypes.string,
  onMouseLeave: PropTypes.func,
};

HoverCell.defaultProps = {
  textToRender: <p />,
  text: '',
  onMouseLeave: () => {},
};

export default HoverCell;
