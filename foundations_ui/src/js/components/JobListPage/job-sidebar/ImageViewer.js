import React from 'react';
import PropTypes from 'prop-types';

export default function ImageViewer(props) {
  return (
    <img
      style={{
        background: 'green',
        margin: 'auto',
        padding: '20px 0px 10px 0px',
        display: 'block',
      }}
      src="https://www.dummyimage.com/500x300"
      alt="dummyimage"
    />
  );
}
