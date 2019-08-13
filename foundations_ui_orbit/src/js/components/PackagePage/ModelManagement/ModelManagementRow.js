import React, { Component } from "react";
import PropTypes from "prop-types";
import ModelManagementDetail from "./ModelManagementDetails";
import ModelRecalibrationModal from "./ModelRecalibrationModal";
import BaseActions from "../../../actions/BaseActions";
import NewModelRecalibrationModal from "./NewModelRecalibrationModal";

const ModelManagementRow = props => {
  const [recalibrateOpen, setRecalibrateOpen] = React.useState(false);

  const clickDetails = () => {
    if (props.isDetail) {
      props.toggleDetailRow(-1);
    } else {
      props.toggleDetailRow(props.rowNum);
    }
  };

  const clickRecalibrate = () => {
    let value = !recalibrateOpen;
    setRecalibrateOpen(value);
  };

  const onChangeDefault = e => {
    if (props.rowData.default === false) {
      let body = {
        default_model: props.rowData.model_name
      };

      BaseActions.putApiary(
        "/projects/" + props.location.state.project.name,
        body
      ).then(result => {
        props.reload();
      });
    }
  };

  const clickActivate = () => {
    let body = {
      model_name: props.rowData.model_name,
      serving: true
    };

    BaseActions.putApiary(
      "/projects/" + props.location.state.project.name,
      body
    ).then(result => {
      props.reload();
    });
  };

  const clickRetire = () => {
    let body = {
      model_name: props.rowData.model_name,
      serving: false
    };

    BaseActions.putApiary(
      "/projects/" + props.location.state.project.name,
      body
    ).then(result => {
      props.reload();
    });
  };

  let entrypoints = "";

  for (var key in props.rowData.entrypoints) {
    entrypoints += key + ": ";
    for (var subkey in props.rowData.entrypoints[key]) {
      entrypoints +=
        subkey + ": " + props.rowData.entrypoints[key][subkey] + " ";
    }
    entrypoints += "; ";
  }

  let validation_metric = "";

  if (props.rowData.validation_metrics) {
    for (var key in props.rowData.validation_metrics) {
      validation_metric +=
        key + ": " + props.rowData.validation_metrics[key] + "; ";
    }
  }

  return (
    <div className="model-management-row">
      <div className="model-management-cell">
        <input
          className="model-checkbox-default"
          type="checkbox"
          onClick={onChangeDefault}
          checked={props.rowData.default === true}
        />
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{props.rowData.model_name}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{props.rowData.created_at}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{props.rowData.created_by}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{props.rowData.description || ""}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{entrypoints}</p>
      </div>
      <div className="model-management-cell">
        <p
          className={
            props.rowData.status === "Active" ? "hide-text active" : "hide-text"
          }
        >
          {props.rowData.status}
        </p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{validation_metric}</p>
      </div>
      <div className="model-management-cell">
        <div className="container-cell-buttons">
          <button className="b--secondary-text" onClick={clickRecalibrate}>
            recalibrate
          </button>
          <button
            className="b--secondary-text"
            onClick={
              props.rowData.status === "activated" ? clickRetire : clickActivate
            }
          >
            {props.rowData.status === "activated" ? "retire" : "activate"}
          </button>
          <button
            className={
              props.isDetail ? "b--secondary-text active" : "b--secondary-text"
            }
            onClick={clickDetails}
          >
            {props.isDetail === true ? (
              <i class="arrow up" />
            ) : (
              <i class="arrow down" />
            )}
            <span>details</span>
          </button>
        </div>
      </div>
      {props.isDetail === true && (
        <ModelManagementDetail model={props.rowData} />
      )}
      {recalibrateOpen === true && (
        <NewModelRecalibrationModal
          onClose={clickRecalibrate}
          model={props.rowData}
          reload={props.reload}
          {...props}
        />
      )}
    </div>
  );
};

ModelManagementRow.propTypes = {
  rowData: PropTypes.object,
  isDetail: PropTypes.bool,
  toggleDetailRow: PropTypes.func,
  rowNum: PropTypes.number,
  isRecalibrate: PropTypes.bool,
  location: PropTypes.object,
  reload: PropTypes.func
};

ModelManagementRow.defaultProps = {
  rowData: {},
  isDetail: false,
  toggleDetailRow: () => {},
  rowNum: -1,
  isRecalibrate: false
};

export default ModelManagementRow;
