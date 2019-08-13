import React, { Component } from "react";
import PropTypes from "prop-types";
import moment from "moment";

const ModelManagementDetails = props => {
  const renderEntrypoints = () => {
    let entrypoints = [];
    let i = 0;

    for (var key in props.model.entrypoints) {
      let entrypointString = "";
      entrypointString += key + ": ";
      for (var subkey in props.model.entrypoints[key]) {
        entrypointString +=
          subkey + ": " + props.model.entrypoints[key][subkey] + ", ";
      }
      entrypoints.push(
        <p className="model-management-details-entrypoint">
          {entrypointString}
        </p>
      );

      i++;
    }

    return entrypoints;
  };

  const renderValidationMetrics = () => {
    let validation_metrics = [];

    if (props.model.validation_metrics) {
      for (var key in props.model.validation_metrics) {
        validation_metrics.push(
          <p className="model-management-details-entrypoint">
            {key + ": " + props.model.validation_metrics[key]}
          </p>
        );
      }
    }

    return validation_metrics;
  };

  return (
    <div className="model-management-details-container">
      <p className="model-management-details-header font-bold text-upper">
        Model Properties
      </p>
      <div className="model-management-details-upper-container">
        <div>
          <p className="model-management-details-text-label font-bold">
            Model Name:
          </p>
          <p className="model-management-details-text">
            {props.model.model_name}
          </p>
          <p className="model-management-details-text-label font-bold">
            Status:
          </p>
          <p className="model-management-details-text">{props.model.status}</p>
          <p className="model-management-details-text-label font-bold">
            Default:
          </p>
          <p className="model-management-details-text">
            {props.model.default === true ? "true" : "false"}
          </p>
        </div>
        <div>
          <p className="model-management-details-text-label font-bold">
            Model Description:
          </p>
          <p className="model-management-details-text">
            {props.model.description || ""}
          </p>
          <p className="model-management-details-text-label font-bold">
            Created at:
          </p>
          <p className="model-management-details-text">
            {moment(props.model.created_at)
              .format("YYYY-MM-DD HH:mm")
              .toString()}
          </p>
          <p className="model-management-details-text-label font-bold">
            Created By:
          </p>
          <div className="model-management-details-text">
            {props.model.created_by}
          </div>
        </div>
      </div>
      <div className="model-management-details-lower-container">
        <div>
          <p className="model-management-details-text-label font-bold">
            Validation Metrics:
          </p>
          <p className="model-management-details-entrypoints-container">
            {renderValidationMetrics()}
          </p>
        </div>
        <div>
          <p className="model-management-details-text-label font-bold">
            Entrypoints:
          </p>
          <div className="model-management-details-entrypoints-container">
            {renderEntrypoints()}
          </div>
        </div>
      </div>
    </div>
  );
};

ModelManagementDetails.propTypes = {
  model: PropTypes.object
};

ModelManagementDetails.defaultProps = {
  model: {}
};

export default ModelManagementDetails;
