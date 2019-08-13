import React, { Component } from "react";
import PropTypes from "prop-types";

class PackagePageHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pageName: this.props.pageName,
      pageSubName: this.props.pageSubName
    };
  }

  render() {
    const { pageName, pageSubName } = this.state;
    return (
      <div className="layout-package-header-container">
        <h2 className="font-bold">{pageName}</h2>
        <h3>{pageSubName}</h3>
      </div>
    );
  }
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
