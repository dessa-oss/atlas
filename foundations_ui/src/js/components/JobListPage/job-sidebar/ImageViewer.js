import React from 'react';
import PropTypes from 'prop-types';

export default function ImageViewer(props) {
  const { image } = props;

  return (
    <img
      className="media"
      src={image}
      alt="Could not find artifact"
    />
  );
}

ImageViewer.propTypes = {
  image: PropTypes.string.isRequired,
};
