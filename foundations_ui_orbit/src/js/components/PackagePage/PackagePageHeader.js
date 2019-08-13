import React, { Component } from "react";
import PropTypes from "prop-types";

const PackagePageHeader = props => {
  return (
    <div className="layout-package-header-container">
      <h2 className="font-bold">{props.pageName}</h2>
      <h3>{props.pageSubName}</h3>
    </div>
  );
}

PackagePageHeader.propTypes = {
  pageName: PropTypes.string,
  pageSubName: PropTypes.string
};

PackagePageHeader.defaultProps = {
  pageName: "",
  pageSubName: ""
};

export default PackagePageHeader;
