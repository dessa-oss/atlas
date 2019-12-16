import React from 'react';
import PropTypes from 'prop-types';

const Loading = props => {
  const { loadingMessage, floating } = props;
  const floatingClass = floating ? 'floating' : '';

  return (
    <div className={`loading-container ${floatingClass}`}>
      <div id="circle-orbit-container">
        <div id="sun" />
        <div id="first-orbit">
          <div className="first-orbit-circle" />
        </div>
        <div id="second-orbit">
          <div className="second-orbit-circles" />
        </div>
        <div id="third-orbit">
          <div className="third-orbit-circles" />
        </div>
      </div>
      <p>{loadingMessage}</p>
    </div>
  );
};

Loading.propTypes = {
  loadingMessage: PropTypes.string,
  floating: PropTypes.bool,
};

Loading.defaultProps = {
  loadingMessage: '',
  floating: false,
};

export default Loading;
