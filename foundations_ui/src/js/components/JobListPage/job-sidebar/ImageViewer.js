import React from 'react';
import PropTypes from 'prop-types';

export default function ImageViewer(props) {
  const { image } = props;

  return (
    <img
      className="image-viewer"
      src={image}
      alt="No artifacts exist"
    />
  );
}

ImageViewer.propTypes = {
  image: PropTypes.string,
};

ImageViewer.defaultProps = {
  image: 'ImageViewer: No image prop.',
};
