import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import EditPredictor from "./EditPredictor.js";
import { Modal, ModalBody } from "reactstrap";
import BaseActions from "../../../actions/BaseActions.js";

const Predictors = props => {
  const [open, setOpen] = React.useState(false);
  const [expanded, setExpanded] = React.useState(false);
  const [proportion, setProportion] = React.useState(props.proportion);
  const [editable, setEditable] = React.useState(false);
  const statuses = ["Running", "Test", "Retire"];

  const [selectedStatus, setSelectedStatus] = React.useState(() => {
    let value = "Running";
    if (props.predictor.status === "retired") {
      value = "Retire";
    } else if (props.predictor.status === "testing") {
      value = "Test";
    }

    return value;
  });

  const onclickEdit = () => {
    setOpen(true);
  };

  const onClickCloseEditPredictor = () => {
    setOpen(false);
  };

  const onClickSavePredictor = data => {
    setOpen(false);
    props.savePredictor(data);
  };

  const onclickRetire = () => {
    BaseActions.postJSONFile(
      "files/predictors/retire",
      "predictors.json",
      props.predictor.name
    ).then(result => {
      props.reload();
    });
  };

  const onClickActivate = () => {
    BaseActions.postJSONFile(
      "files/predictors/activate",
      "predictors.json",
      props.predictor.name
    ).then(result => {
      props.reload();
    });
  };

  const onclickDetails = () => {
    let prevExpanded = expanded;
    setExpanded(!prevExpanded);
  };

  const onclickRemove = () => {
    BaseActions.postJSONFile(
      "files/predictors/delete",
      "predictors.json",
      props.predictor.name
    ).then(result => {
      props.reload();
    });
  };

  const onChangeProportion = e => {
    setProportion(e.target.value);
  };

  const onClickEditProportion = () => {
    setEditable(true);
  };

  const onKeyDown = e => {
    if (e.key === "Enter") {
      let value = parseFloat(proportion);

      if (!isNaN(value) && value >= 0 && value <= 1) {
        setProportion(e.target.value);
        props.changeProportion(props.predictor, value);
        setEditable(false);
      }
    }
  };

  let actions_string = props.predictor.action_space[0];

  for (let i = 1; i < props.predictor.action_space.length; i++) {
    actions_string += ", " + props.predictor.action_space[i];
  }

  let labelClassName = "label";

  if (props.method === "Define Manually") {
    if (expanded) {
      if (parseFloat(proportion) !== parseFloat(props.proportion)) {
        labelClassName = "label expanded edited";
      } else {
        labelClassName = "label expanded";
      }
    } else {
      if (parseFloat(proportion) !== parseFloat(props.proportion)) {
        labelClassName = "label edited";
      }
    }
  }

  const runningPredictors = props.predictors.filter(
    item => item.status === "running"
  );

  let proportionValue = "auto";

  if (props.predictor.status !== "testing") {
    if (props.predictor.status !== "running") {
      proportionValue = (proportion * 100).toFixed(0) + "%";
    } else {
      if (props.splitMechanism === "Random split (even)") {
        proportionValue = (100 / runningPredictors.length).toFixed(0) + "%";
      } else {
        if (props.method === "Define Manually") {
          proportionValue = (proportion * 100).toFixed(0) + "%";
        }
      }
    }
  }

  const onChangeStatus = e => {
    let newValue = e.target.value;
    let predictor = props.predictor;
    if (newValue === "Running") {
      predictor.status = "running";
    } else if (newValue === "Test") {
      predictor.status = "testing";
    } else if (newValue === "Retire") {
      predictor.status = "retired";
    }

    delete predictor.proportion;

    let data = {
      predictor: predictor,
      split_mechanism: props.splitMechanism
    };

    BaseActions.postJSONFile(
      "files/predictors/edit",
      "predictors.json",
      data
    ).then(result => {
      setSelectedStatus(newValue);
      props.reload();
    });
  };

  let statusClassName = "pred-active";
  let circleStatusClasssName = "circle-status active";

  if (props.predictor.status === "retired") {
    statusClassName = "pred-retired";
    circleStatusClasssName = "circle-status retired";
  } else if (props.predictor.status === "testing") {
    statusClassName = "pred-testing";
    circleStatusClasssName = "circle-status testing";
  }

  return (
    <div
      className={
        expanded === false
          ? props.predictors.length <= 2
            ? props.predictors.length <= 1
              ? "container-row-parent just-one"
              : "container-row-parent less-amount"
            : "container-row-parent"
          : props.predictors.length <= 2
          ? props.predictors.length <= 1
            ? "container-row-parent just-one expanded"
            : "container-row-parent less-amount expanded"
          : "container-row-parent expanded"
      }
    >
      <div className="i--icon-blue-arrow">
        <div className="arrow-line" />
      </div>
      <div className="container-pred-row">
        <div className="container-pred-percentage">
          {editable === true ? (
            <input
              className={expanded === true ? "input expanded" : "input"}
              onChange={onChangeProportion}
              value={proportion}
              onKeyDown={onKeyDown}
            />
          ) : (
            <p className={labelClassName}>{proportionValue}</p>
          )}
          {props.method === "Define Manually" &&
            props.splitMechanism !== "Random split (even)" &&
            props.predictor.status === "running" && (
              <button
                type="button"
                disabled={props.method !== "Define Manually"}
                onClick={onClickEditProportion}
                className={
                  expanded === true
                    ? "button-edit-proportion expanded"
                    : "text-upper button-edit-proportion"
                }
              >
                <i className="i--icon-pencil-dark" />
              </button>
            )}
        </div>
        <div
          className={
            expanded === false
              ? "container-pred-grid"
              : "container-pred-grid pred-separator"
          }
        >
          <div className="container-pred-info pred-column-1">
            <span className="span">Name: </span>
            <span>{props.predictor.name || ""}</span>
          </div>
          {/* <div className="container-pred-info container-status pred-column-2">
            <span className="pred-status span">Status:</span>
            <span className={statusClassName}>
              {props.predictor.status || ""}
            </span>
            <div className={circleStatusClasssName} />
          </div> */}
          <div className="container-pred-buttons container-buttons pred-column-3">
            <div className="select-container">
              <select
                value={selectedStatus}
                onChange={onChangeStatus}
                className={`select-status ${statusClassName}`}
              >
                <span>lol</span>
                {statuses.map(item => {
                  return <option>{item}</option>;
                })}
              </select>
              <div className={`select-status-circle ${statusClassName}`} />
            </div>
            <button className="b--secondary" onClick={onclickEdit}>
              <div className="i--icon-pencil-grey" />
            </button>
            {/* <button
              className="b--secondary-text"
              onClick={
                props.predictor.status === "retired"
                  ? onClickActivate
                  : onclickRetire
              }
            >
              {props.predictor.status === "retired" ? "activate" : "retire"}
            </button> */}
            <button
              className={
                expanded ? "b--secondary-text active" : "b--secondary-text"
              }
              onClick={onclickDetails}
            >
              {expanded ? <i class="arrow up" /> : <i class="arrow down" />}
              <span>details</span>
            </button>
            <button className="b--secondary red" onClick={onclickRemove}>
              <div className="close" />
            </button>
          </div>
          {/* {expanded === true && ( */}
          <div
            className={
              expanded
                ? "more-detail-container expanded"
                : "more-detail-container"
            }
          >
            <div>
              <div className="container-pred-info pred-column-1 expanded-notes ">
                <div>
                  <p className="label">Model Package Name:</p>
                  <p className="info">{props.predictor.model_package_name}</p>
                </div>
                <div>
                  <p className="label">Environment:</p>
                  <p className="info">{props.predictor.environment}</p>
                </div>
              </div>
              <div className="container-pred-info pred-column-2 expanded-notes ">
                <div>
                  <p className="label">Action Space:</p>
                  <p className="info">{actions_string}</p>
                </div>
              </div>

              <div className="container-pred-info container-status pred-column-3 expanded-notes ">
                <div>
                  <p className="label">Post Prediction Selection:</p>
                  <p className="info">
                    Uncertainty scoring:{" "}
                    {
                      props.predictor.post_predict_selection
                        .exploration_strategy
                    }
                  </p>
                  <p className="info">
                    Uncertainty handle: exploration{" "}
                    {props.predictor.post_predict_selection
                      .exploration_percentage * 100}
                    %
                  </p>
                </div>
              </div>
            </div>
            <div className="container-pred-info container-status pred-column-1 notes">
              <div>
                <p className="label">Notes:</p>
                <p className="info">{props.predictor.description}</p>
              </div>
            </div>
          </div>
          {/* )} */}
        </div>
      </div>
      <Modal
        isOpen={open}
        toggle={onClickCloseEditPredictor}
        className={"add-predictor-modal-container"}
      >
        <ModalBody>
          <EditPredictor
            predictor={props.predictor}
            onClose={onClickCloseEditPredictor}
            reload={props.reload}
            splitMechanism={props.splitMechanism}
          />
        </ModalBody>
      </Modal>
    </div>
  );
};

Predictors.propTypes = {
  predictor: PropTypes.object,
  savePredictor: PropTypes.func,
  proportion: PropTypes.number,
  method: PropTypes.string,
  changeProportion: PropTypes.func,
  predictors: PropTypes.array,
  splitMechanism: PropTypes.string,
  reload: PropTypes.func
};

Predictors.defaultProps = {
  predictor: {},
  proportion: 0,
  method: "Define Manually",
  splitMechanism: "spec",
  predictors: []
};

export default withRouter(Predictors);
