import React from "react";
import PropTypes from "prop-types";

const Loading = props => {
  const { loadingMessage } = props;

  return (
    <div className="loading-container">
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
  loadingMessage: PropTypes.string
};

Loading.defaultProps = {
  loadingMessage: ""
};

export default Loading;
