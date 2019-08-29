import React from 'react';
import PropTypes from 'prop-types';

class Tag extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value: this.props.value,
    };
  }

  render() {
    const { value } = this.state;

    return (
      value === 'tf' ? <div className="job-tag i--icon-tf" />
        : <div className="job-tag">{value}<div className="close-button" /></div>
    );
  }
}

Tag.propTypes = {
  value: PropTypes.string,
};

Tag.defaultProps = {
  value: '',
};

export default Tag;
