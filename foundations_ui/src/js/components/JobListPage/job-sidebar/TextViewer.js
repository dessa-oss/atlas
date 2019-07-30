import React from 'react';
import PropTypes from 'prop-types';

export default function TextViewer(props) {
  const { text } = props;

  return (
    <p>{text}</p>
  );
}


TextViewer.propTypes = {
  text: PropTypes.string,
};

TextViewer.defaultProps = {
  text: 'No artifacts for this job',
};
