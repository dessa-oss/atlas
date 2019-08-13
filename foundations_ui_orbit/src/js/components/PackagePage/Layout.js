import React, { Component, Children } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PackageToolbar from "./PackageToolbar";
import SideBar from "./SideBar";

const Layout = props => {
  const [loading, setLoading] = React.useState(false);
  const [loadingMessage, setLoadingMessage] = React.useState("");

  const onLoading = (value, message) => {
    setLoading(value);
    setLoadingMessage(message);
  };

  return (
    <div className="container-layout">
      <PackageToolbar
        tab={props.tab}
        project={props.location.state.project}
        title={props.title}
        onLoading={onLoading}
      />
      <div className="container-sidebar-children">
        <SideBar tab={props.tab} />
        <div className="container-children">{props.children}</div>
      </div>
      {loading === true && (
        <div className="container-loading">
          <div className="container-loading-message">{loadingMessage}</div>
        </div>
      )}
    </div>
  );
};

Layout.propTypes = {
  tab: PropTypes.string,
  history: PropTypes.object,
  project: PropTypes.object,
  title: PropTypes.string
};

Layout.defaultProps = {
  tab: "Deployment",
  title: "Deployment"
};

export default withRouter(Layout);
