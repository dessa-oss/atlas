import React from "react";
import { withRouter } from "react-router-dom";
import { get } from "../../../actions/BaseActions";

const Metadata = () => {
  const [deploymentMetadata, setDeploymentMetadata] = React.useState({});
  const [expanded, setExpanded] = React.useState(false);

  React.useEffect(() => {
    get("metadata").then(result => {
      if (result && result.data) {
        setDeploymentMetadata(result.data);
      }
    });
  }, []);

  const renderRows = () => {
    const rows = [];

    Object.keys(deploymentMetadata).forEach(key => {
      rows.push(
        <div className="container-metadata">
          <p className="label-metadata-key">{key}: </p>
          <p className="label-metadata-value">{deploymentMetadata[key]}</p>
        </div>
      );
    });

    return rows;
  };

  const onclickDetails = () => {
    const prevExpanded = expanded;
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
        <button type="button" className="b--secondary" onClick={onclickDetails}>
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
