import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import EditPredictor from "./EditPredictor";
import { Modal, ModalBody } from "reactstrap";
import { postJSONFile } from "../../../actions/BaseActions";

const Predictors = props => {
  const [open, setOpen] = React.useState(false);
  const [expanded, setExpanded] = React.useState(false);
  const [selectedProportion, setSelectedProportion] = React.useState(() => {
    const { proportion } = props;
    return proportion;
  });
  const [editable, setEditable] = React.useState(false);
  const statuses = ["Running", "Test", "Retire"];

  const [selectedStatus, setSelectedStatus] = React.useState(() => {
    const { predictor } = props;

    let value = "Running";
    if (predictor.status === "retired") {
      value = "Retire";
    } else if (predictor.status === "testing") {
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

  const onclickDetails = () => {
    const prevExpanded = expanded;
    setExpanded(!prevExpanded);
  };

  const onclickRemove = () => {
    const { predictor, reload } = props;
    postJSONFile(
      "files/predictors/delete",
      "predictors.json",
      predictor.name
    ).then(() => {
      reload();
    });
  };

  const onChangeProportion = e => {
    setSelectedProportion(e.target.value);
  };

  const onClickEditProportion = () => {
    setEditable(true);
  };

  const onKeyDown = e => {
    const { changeProportion, predictor } = props;

    if (e.key === "Enter") {
      const value = parseFloat(selectedProportion);

      if (!Number.isNaN(value) && value >= 0 && value <= 1) {
        setSelectedProportion(e.target.value);
        changeProportion(predictor, value);
        setEditable(false);
      }
    }
  };

  const onChangeStatus = e => {
    const newValue = e.target.value;
    const { predictor, splitMechanism, reload } = props;
    if (newValue === "Running") {
      predictor.status = "running";
    } else if (newValue === "Test") {
      predictor.status = "testing";
    } else if (newValue === "Retire") {
      predictor.status = "retired";
    }

    delete predictor.proportion;

    const data = {
      predictor: predictor,
      split_mechanism: splitMechanism
    };

    postJSONFile(
      "files/predictors/edit",
      "predictors.json",
      data
    ).then(() => {
      setSelectedStatus(newValue);
      reload();
    });
  };

  const {
    proportion, predictor, predictors, method, splitMechanism, reload
  } = props;

  let actionsString = predictor.action_space[0];

  for (let i = 1; i < predictor.action_space.length; i += 1) {
    actionsString += `, ${predictor.action_space[i]}`;
  }

  let labelClassName = "label";


  if (method === "Define Manually") {
    if (expanded) {
      if (parseFloat(selectedProportion) !== parseFloat(proportion)) {
        labelClassName = "label expanded edited";
      } else {
        labelClassName = "label expanded";
      }
    } else if (parseFloat(selectedProportion) !== parseFloat(proportion)) {
      labelClassName = "label edited";
    }
  }

  const runningPredictors = predictors.filter(
    item => item.status === "running"
  );

  let proportionValue = "auto";

  if (predictor.status !== "testing") {
    if (predictor.status !== "running") {
      proportionValue = `${(selectedProportion * 100).toFixed(0)}%`;
    } else if (splitMechanism === "Random split (even)") {
      proportionValue = `${(100 / runningPredictors.length).toFixed(0)}%`;
    } else if (method === "Define Manually") {
      proportionValue = `${(selectedProportion * 100).toFixed(0)}%`;
    }
  }


  let statusClassName = "pred-active";

  if (predictor.status === "retired") {
    statusClassName = "pred-retired";
  } else if (predictor.status === "testing") {
    statusClassName = "pred-testing";
  }

  let parentClassName = "";

  if (expanded === false) {
    if (predictors.length <= 2) {
      if (predictors.length <= 1) {
        parentClassName = "container-row-parent just-one";
      } else {
        parentClassName = "container-row-parent less-amount";
      }
    } else {
      parentClassName = "container-row-parent";
    }
  } else if (predictors.length <= 2) {
    if (predictors.length <= 1) {
      parentClassName = "container-row-parent just-one expanded";
    } else {
      parentClassName = "container-row-parent less-amount expanded";
    }
  } else {
    parentClassName = "container-row-parent expanded";
  }


  return (
    <div
      className={parentClassName}
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
              value={selectedProportion}
              onKeyDown={onKeyDown}
            />
          ) : (
            <p className={labelClassName}>{proportionValue}</p>
          )}
          {method === "Define Manually"
            && splitMechanism !== "Random split (even)"
            && predictor.status === "running" && (
              <button
                type="button"
                disabled={method !== "Define Manually"}
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
            <span>{predictor.name || ""}</span>
          </div>
          <div className="container-pred-buttons container-buttons pred-column-3">
            <div className="select-container">
              <select
                value={selectedStatus}
                onChange={onChangeStatus}
                className={`select-status ${statusClassName}`}
              >
                <span>lol</span>
                {statuses.map(item => {
                  return <option key={item}>{item}</option>;
                })}
              </select>
              <div className={`select-status-circle ${statusClassName}`} />
            </div>
            <button type="button" className="b--secondary" onClick={onclickEdit}>
              <div className="i--icon-pencil-grey" />
            </button>
            <button
              type="button"
              className={
                expanded ? "b--secondary-text active" : "b--secondary-text"
              }
              onClick={onclickDetails}
            >
              {expanded ? <i className="arrow up" /> : <i className="arrow down" />}
              <span>details</span>
            </button>
            <button type="button" className="b--secondary red" onClick={onclickRemove}>
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
                  <p className="info">{predictor.model_package_name}</p>
                </div>
                <div>
                  <p className="label">Environment:</p>
                  <p className="info">{predictor.environment}</p>
                </div>
              </div>
              <div className="container-pred-info pred-column-2 expanded-notes ">
                <div>
                  <p className="label">Action Space:</p>
                  <p className="info">{actionsString}</p>
                </div>
              </div>

              <div className="container-pred-info container-status pred-column-3 expanded-notes ">
                <div>
                  <p className="label">Post Prediction Selection:</p>
                  <p className="info">
                    Uncertainty scoring:{" "}
                    {
                      predictor.post_predict_selection
                        .exploration_strategy
                    }
                  </p>
                  <p className="info">
                    Uncertainty handle: exploration{" "}
                    {predictor.post_predict_selection
                      .exploration_percentage * 100}
                    %
                  </p>
                </div>
              </div>
            </div>
            <div className="container-pred-info container-status pred-column-1 notes">
              <div>
                <p className="label">Notes:</p>
                <p className="info">{predictor.description}</p>
              </div>
            </div>
          </div>
          {/* )} */}
        </div>
      </div>
      <Modal
        isOpen={open}
        toggle={onClickCloseEditPredictor}
        className="add-predictor-modal-container"
      >
        <ModalBody>
          <EditPredictor
            predictor={predictor}
            onClose={onClickCloseEditPredictor}
            reload={reload}
            splitMechanism={splitMechanism}
          />
        </ModalBody>
      </Modal>
    </div>
  );
};

Predictors.propTypes = {
  predictor: PropTypes.object,
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
  predictors: [],
  changeProportion: () => null,
  reload: () => null
};

export default withRouter(Predictors);
