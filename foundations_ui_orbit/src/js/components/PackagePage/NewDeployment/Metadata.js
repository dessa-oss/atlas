import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import EditPredictor from "./EditPredictor.js";
import { Modal, ModalBody } from "reactstrap";
import BaseActions from "../../../actions/BaseActions.js";

const Metadata = props => {
  const [deploymentMetadata, setDeploymentMetadata] = React.useState({});
  const [expanded, setExpanded] = React.useState(false);

  React.useEffect(() => {
    BaseActions.get("metadata").then(result => {
      setDeploymentMetadata(result.data);
    });
  }, []);

  const renderRows = () => {
    let rows = [];
    for (var key in deploymentMetadata) {
      rows.push(
        <div className="container-metadata">
          <p className="label-metadata-key">{key}: </p>
          <p className="label-metadata-value">{deploymentMetadata[key]}</p>
        </div>
      );
    }

    return rows;
  };

  const onclickDetails = () => {
    let prevExpanded = expanded;
    setExpanded(!prevExpanded);
  };

  return (
    <div
      className={
        expanded ? "metadata-container expanded" : "metadata-container"
      }
    >
      <div>
        <p className="new-dep-section font-bold">DEPLOYMENT METADATA</p>
        <button className="b--secondary" onClick={onclickDetails}>
          <div className="plus-button" />
        </button>
      </div>
      {renderRows()}
    </div>
  );
};

Metadata.propTypes = {};

Metadata.defaultProps = {};

export default withRouter(Metadata);
