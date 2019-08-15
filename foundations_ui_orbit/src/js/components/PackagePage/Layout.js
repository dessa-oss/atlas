import React from "react";
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

  const {
    tab, location, title, children
  } = props;

  return (
    <div className="container-layout">
      <PackageToolbar
        tab={tab}
        project={location.state.project}
        title={title}
        onLoading={onLoading}
      />
      <div className="container-sidebar-children">
        <SideBar tab={tab} />
        <div className="container-children">{children}</div>
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
  title: PropTypes.string,
  location: PropTypes.object,
  children: PropTypes.object
};

Layout.defaultProps = {
  tab: "Deployment",
  title: "Deployment",
  location: { state: {} },
  children: []

};

export default withRouter(Layout);
