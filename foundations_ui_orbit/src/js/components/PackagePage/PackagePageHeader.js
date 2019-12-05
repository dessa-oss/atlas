import React from "react";
import PropTypes from "prop-types";

const PackagePageHeader = props => {
  const { pageName, pageSubName } = props;

  return (
    <div className="layout-package-header-container">
      <h2 className="font-bold">{pageName}</h2>
      <h3>{pageSubName}</h3>
    </div>
  );
};

PackagePageHeader.propTypes = {
  pageName: PropTypes.string,
  pageSubName: PropTypes.string
};

PackagePageHeader.defaultProps = {
  pageName: "",
  pageSubName: ""
};

export default PackagePageHeader;
