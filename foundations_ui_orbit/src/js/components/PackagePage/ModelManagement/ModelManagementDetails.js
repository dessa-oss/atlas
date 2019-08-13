import React, { Component } from "react";
import PropTypes from "prop-types";
import moment from "moment";

class ModelManagementDetails extends Component {
  constructor(props) {
    super(props);

    let entrypoints = "";

    let validation_metrics = "";

    if (this.props.model.validation_metrics) {
      for (var key in this.props.model.validation_metrics) {
        validation_metrics +=
          key + ": " + this.props.model.validation_metrics[key] + "\n";
      }
    }

    this.state = {
      entrypoints: entrypoints,
      validation_metrics: validation_metrics
    };
  }

  renderEntrypoints() {
    let entrypoints = [];
    let i = 0;

    for (var key in this.props.model.entrypoints) {
      let entrypointString = "";
      entrypointString += key + ": ";
      for (var subkey in this.props.model.entrypoints[key]) {
        entrypointString +=
          subkey + ": " + this.props.model.entrypoints[key][subkey] + ", ";
      }
      entrypoints.push(
        <p className="model-management-details-entrypoint">
          {entrypointString}
        </p>
      );

      i++;
    }

    return entrypoints;
  }

  renderValidationMetrics() {
    let validation_metrics = [];

    if (this.props.model.validation_metrics) {
      for (var key in this.props.model.validation_metrics) {
        validation_metrics.push(
          <p className="model-management-details-entrypoint">
            {key + ": " + this.props.model.validation_metrics[key]}
          </p>
        );
      }
    }

    return validation_metrics;
  }

  render() {
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
              {this.props.model.model_name}
            </p>
            <p className="model-management-details-text-label font-bold">
              Status:
            </p>
            <p className="model-management-details-text">
              {this.props.model.status}
            </p>
            <p className="model-management-details-text-label font-bold">
              Default:
            </p>
            <p className="model-management-details-text">
              {this.props.model.default === true ? "true" : "false"}
            </p>
          </div>
          <div>
            <p className="model-management-details-text-label font-bold">
              Model Description:
            </p>
            <p className="model-management-details-text">
              {this.props.model.description || ""}
            </p>
            <p className="model-management-details-text-label font-bold">
              Created at:
            </p>
            <p className="model-management-details-text">
              {moment(this.props.model.created_at)
                .format("YYYY-MM-DD HH:mm")
                .toString()}
            </p>
            <p className="model-management-details-text-label font-bold">
              Validation Metrics:
            </p>
            <div className="model-management-details-entrypoints-container">
              {this.renderValidationMetrics()}
            </div>
          </div>
        </div>
        <div className="model-management-details-lower-container">
          <div>
            <p className="model-management-details-text-label font-bold">
              Created By:
            </p>
            <p className="model-management-details-text">
              {this.props.model.created_by}
            </p>
          </div>
          <div>
            <p className="model-management-details-text-label font-bold">
              Entrypoints:
            </p>
            <div className="model-management-details-entrypoints-container">
              {this.renderEntrypoints()}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ModelManagementDetails.propTypes = {
  model: PropTypes.object
};

ModelManagementDetails.defaultProps = {
  model: {}
};

export default ModelManagementDetails;
