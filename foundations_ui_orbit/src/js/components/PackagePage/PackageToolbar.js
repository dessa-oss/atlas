import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PackagePageHeader from "./PackagePageHeader";

class PackageToolbar extends React.Component {
  render() {
    const { project, title } = this.props;
    return (
      <div className="layout-package-toolbar-container">
        <div className="job-header-logo-container">
          <div className="i--icon-logo" />
          <PackagePageHeader
            pageName={project.name}
            pageSubName={
              title === ""
                ? "Inference Automation and Model Management"
                : title
            }
          />
        </div>
      </div>
    );
  }
}

PackageToolbar.propTypes = {
  project: PropTypes.object,
  title: PropTypes.string,
  onLoading: PropTypes.func
};

PackageToolbar.defaultProps = {
  project: {},
  title: "",
  onLoading: () => null
};

export default withRouter(PackageToolbar);
