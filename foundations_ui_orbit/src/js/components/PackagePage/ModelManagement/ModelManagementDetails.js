import React from "react";
import PropTypes from "prop-types";
import moment from "moment";

const ModelManagementDetails = props => {
  const { model } = props;

  const renderEntrypoints = () => {
    const entrypoints = [];

    Object.keys(model.entrypoints).forEach(key => {
      const entrypointString = `${key}: `;
      Object.keys(model.entrypoints[key]).forEach(subkey => {
        entrypointString.concat(subkey.concat(`: ${model.entrypoints[key][subkey]}, `));
      });
      entrypoints.push(
        <p className="model-management-details-entrypoint">
          {entrypointString}
        </p>
      );
    });

    return entrypoints;
  };

  const renderValidationMetrics = () => {
    const validationMetrics = [];

    if (model.validationMetrics) {
      Object.keys(model.validationMetrics).forEach(key => {
        validationMetrics.push(
          <p className="model-management-details-entrypoint">
            {`${key}: ${model.validationMetrics[key]}`}
          </p>
        );
      });
    }

    return validationMetrics;
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
            {model.model_name}
          </p>
          <p className="model-management-details-text-label font-bold">
            Status:
          </p>
          <p className="model-management-details-text">{model.status}</p>
          <p className="model-management-details-text-label font-bold">
            Default:
          </p>
          <p className="model-management-details-text">
            {model.default === true ? "true" : "false"}
          </p>
        </div>
        <div>
          <p className="model-management-details-text-label font-bold">
            Model Description:
          </p>
          <p className="model-management-details-text">
            {model.description || ""}
          </p>
          <p className="model-management-details-text-label font-bold">
            Created at:
          </p>
          <p className="model-management-details-text">
            {moment(model.created_at)
              .format("YYYY-MM-DD HH:mm")
              .toString()}
          </p>
          <p className="model-management-details-text-label font-bold">
            Created By:
          </p>
          <div className="model-management-details-text">
            {model.created_by}
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
