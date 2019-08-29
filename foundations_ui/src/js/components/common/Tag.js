import React from 'react';
import PropTypes from 'prop-types';

class Tag extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value: this.props.value,
    };
  }

  onKeyDown() {}

  render() {
    const { value } = this.state;
    const { removeVisible, removeTag } = this.props;

    return (
      value === 'tf' ? <div className="job-tag i--icon-tf" />
        : (
          <div className="job-tag">{value}
            {removeVisible === true
            && (
              <div
                className="close-button"
                onClick={removeTag}
                role="button"
                aria-label="Close"
                onKeyDown={this.onKeyDown}
                tabIndex={0}
              />
            )}
          </div>
        )
    );
  }
}

Tag.propTypes = {
  value: PropTypes.string,
  removeVisible: PropTypes.bool,
  removeTag: PropTypes.func,
};

Tag.defaultProps = {
  value: '',
  removeVisible: false,
  removeTag: () => null,
};

export default Tag;
