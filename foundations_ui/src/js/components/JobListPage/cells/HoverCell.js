import React, { Component } from 'react';
import PropTypes from 'prop-types';

class HoverCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: this.props.textToRender,
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
  text: PropTypes.string,
};

HoverCell.defaultProps = {
  textToRender: <p />,
  text: '',
};

export default HoverCell;
