import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import Manager from "./Manager";
import Predictors from "./Predictors";
import { Modal, ModalBody } from "reactstrap";
import AddPredictor from "./AddPredictor";
import Schedule from "./Schedule";
import Metadata from "./Metadata";
import PredictorChart from "./PredictorChart";
import BaseActions from "../../../actions/BaseActions";
import PredictorRow from "./PredictorRow";

const NewDeploymentPage = props => {
  const [testLearningConfig, setTestLearningConfig] = React.useState({
    setting: {
      method: "",
      split_mechanism: "",
      feedback_cycle: "",
      hold_out_period_length: 0,
      hold_out_period_unit: ""
    },
    populations: []
  });
  const [newTestLearnConfig, setNewTestLearningConfig] = React.useState({
    setting: {
      method: "",
      split_mechanism: "",
      feedback_cycle: "",
      hold_out_period_length: 0,
      hold_out_period_unit: ""
    },
    populations: []
  });

  const [predictors, setPredictors] = React.useState([]);
  const [newPredictors, setNewPredictors] = React.useState([]);
  const [openAddPredictor, setOpenAddPredictor] = React.useState(false);
  const [openChart, setOpenChart] = React.useState(false);

  const [errorManager, setErrorManager] = React.useState("");
  const [errorProportions, setErrorProportions] = React.useState("");
  const [messageProportions, setMessageProportions] = React.useState("");

  const methods = ["Define Manually", "Automatically Optimize"];

  const manualSpliMechanisms = [
    "Random split (specified proportion)",
    "Random split (even)"
  ];

  const autoSplitMechanisms = ["Multi-arm bandit"];

  const feedbackCycles = [
    "Hourly",
    "Daily",
    "Weekly",
    "Bi-Weekly",
    "Monthly",
    "Quaterly",
    "Semy-Annually"
  ];

  const periodUnits = ["Hour", "Day", "Week", "Month"];

  const reload = () => {
    BaseActions.get("learn").then(result => {
      if (result.data.setting && result.data.populations) {
        setTestLearningConfig(result.data);
        setNewTestLearningConfig(result.data);

        BaseActions.get("predictors").then(resultPredictors => {
          if (resultPredictors.data) {
            let values = resultPredictors.data;
            if (values.length === 1) {
              values[0].proportion = 1;
            } else if (values.length > 1) {
              let newPredictors = values.map(predictor => {
                const filteredPopulations = result.data.populations.filter(
                  item => item.name === predictor.name
                );
                if (filteredPopulations.length >= 1) {
                  predictor.proportion = filteredPopulations[0].proportion;
                }
                return predictor;
              });
            }

            setPredictors(values);
            setNewPredictors([]);
            setNewPredictors(values);
          }
        });
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onChangeMethod = e => {
    let method = newTestLearnConfig.setting.method;

    method = e.target.value;
    let split_mechanism = "Multi-arm bandit";

    if (e.target.value === "Define Manually") {
      split_mechanism = "Random split (specified proportion)";
    }

    setNewTestLearningConfig({
      setting: {
        method: method,
        split_mechanism: split_mechanism,
        feedback_cycle: newTestLearnConfig.setting.feedback_cycle,
        hold_out_period_length:
          newTestLearnConfig.setting.hold_out_period_length,
        hold_out_period_unit: newTestLearnConfig.setting.hold_out_period_unit
      },
      populations: newTestLearnConfig.populations
    });
  };

  const onChangeSplitMechanism = e => {
    let split_mechanism = newTestLearnConfig.setting.split_mechanism;

    split_mechanism = e.target.value;

    setNewTestLearningConfig({
      setting: {
        method: newTestLearnConfig.setting.method,
        split_mechanism: split_mechanism,
        feedback_cycle: newTestLearnConfig.setting.feedback_cycle,
        hold_out_period_length:
          newTestLearnConfig.setting.hold_out_period_length,
        hold_out_period_unit: newTestLearnConfig.setting.hold_out_period_unit
      },
      populations: newTestLearnConfig.populations
    });
  };

  const onChangeFeedbackCycle = e => {
    let feedback_cycle = newTestLearnConfig.setting.feedback_cycle;

    feedback_cycle = e.target.value;

    setNewTestLearningConfig({
      setting: {
        method: newTestLearnConfig.setting.method,
        split_mechanism: newTestLearnConfig.setting.split_mechanism,
        feedback_cycle: feedback_cycle,
        hold_out_period_length:
          newTestLearnConfig.setting.hold_out_period_length,
        hold_out_period_unit: newTestLearnConfig.setting.hold_out_period_unit
      },
      populations: newTestLearnConfig.populations
    });
  };

  const onChangePeriodUnit = e => {
    let hold_out_period_unit = newTestLearnConfig.setting.hold_out_period_unit;

    hold_out_period_unit = e.target.value;

    setNewTestLearningConfig({
      setting: {
        method: newTestLearnConfig.setting.method,
        split_mechanism: newTestLearnConfig.setting.split_mechanism,
        feedback_cycle: newTestLearnConfig.setting.feedback_cycle,
        hold_out_period_length:
          newTestLearnConfig.setting.hold_out_period_length,
        hold_out_period_unit: hold_out_period_unit
      },
      populations: newTestLearnConfig.populations
    });
  };

  const onChangePeriodLength = e => {
    let hold_out_period_length =
      newTestLearnConfig.setting.hold_out_period_length;

    hold_out_period_length = e.target.value;

    setNewTestLearningConfig({
      setting: {
        method: newTestLearnConfig.setting.method,
        split_mechanism: newTestLearnConfig.setting.split_mechanism,
        feedback_cycle: newTestLearnConfig.setting.feedback_cycle,
        hold_out_period_length: hold_out_period_length,
        hold_out_period_unit: newTestLearnConfig.setting.hold_out_period_unit
      },
      populations: newTestLearnConfig.populations
    });
  };

  const onClickCancel = () => {
    setNewTestLearningConfig(testLearningConfig);
  };

  const validate = () => {
    let validated = true;
    let message = "";

    let periodLengthValue = parseInt(
      newTestLearnConfig.setting.hold_out_period_length
    );

    if (isNaN(periodLengthValue)) {
      validated = false;
      message = "Period length must be an integer";
    }

    setErrorManager(message);
    return validated;
  };

  const onClickSave = () => {
    setErrorManager("");

    if (validate()) {
      let periodLengthValue = parseInt(
        newTestLearnConfig.setting.hold_out_period_length
      );

      BaseActions.postJSONFile(
        "learn",
        "test_learn_config.json",
        newTestLearnConfig.setting
      ).then(result => {
        reload();
      });
    }
  };

  const onClickSaveProportions = () => {
    setErrorProportions("");
    setMessageProportions("");
    let result = 0;
    newPredictors.forEach(item => {
      result += item.proportion;
    });

    if (result !== 1) {
      setErrorProportions(
        "Please make sure that the sum of all proportions is equal to 1 (100%)"
      );
    } else {
      let data = newPredictors.map(item => {
        return {
          name: item.name,
          proportion: item.proportion
        };
      });

      BaseActions.postJSONFile(
        "files/proportions",
        "test_learn_config.json",
        data
      ).then(result => {
        reload();
        setMessageProportions("Changes saved!");
      });
    }
  };

  const onClickAddPredictor = () => {
    setOpenAddPredictor(true);
  };

  const onClickShowChart = () => {
    setOpenChart(true);
  };

  const onClickCloseAddPredictor = () => {
    setOpenAddPredictor(false);
  };

  const onClickCloseChart = () => {
    setOpenChart(false);
  };

  const onChangePredictorsProportions = newPredictors => {
    setPredictors(newPredictors);
  };

  const onChangeProportion = (predictor, value) => {
    let values = newPredictors;
    values.forEach(item => {
      if (predictor.name === item.name) {
        item.proportion = value;
      }
    });
    setNewPredictors(values);
  };

  const renderSplitMechanisms = () => {
    if (newTestLearnConfig.setting.method === "Define Manually") {
      return manualSpliMechanisms.map(item => {
        return <option>{item}</option>;
      });
    } else {
      return autoSplitMechanisms.map(item => {
        return <option>{item}</option>;
      });
    }
  };

  const renderPredictors = () => {
    let proportion = 0;
    let predictors_count = newPredictors.length;

    return newPredictors.map(predictor => {
      if (newTestLearnConfig.setting.method === "Define Manually") {
        if (predictors_count === 1) {
          proportion = 1;
        } else if (predictors_count > 1) {
          const filteredPopulations = newTestLearnConfig.populations.filter(
            item => item.name === predictor.name
          );
          if (filteredPopulations.length >= 1) {
            proportion = filteredPopulations[0].proportion;
          }
        }
      }
      return (
        <PredictorRow
          predictor={predictor}
          predictors={newPredictors}
          proportion={proportion}
          changeProportion={onChangeProportion}
          method={newTestLearnConfig.setting.method}
          splitMechanism={newTestLearnConfig.setting.split_mechanism}
          reload={reload}
        />
      );
    });
  };

  return (
    <div className="container-manager-predictors">
      <div className="container-manager">
        <div>
          <p className="new-dep-section font-bold">INFERENCE MANAGER</p>
          <p>
            The test and learn manager allows you to run inference on a single
            model or split your input population to run A/B testing.
          </p>
        </div>
        <div className="new-dep-container-options">
          <p className="subheader font-bold">Test & Learn Manager</p>
          <div className="new-dep-container-select">
            <p className="new-dep-p">Method: </p>
            <select
              value={
                newTestLearnConfig && newTestLearnConfig.setting
                  ? newTestLearnConfig.setting.method
                  : ""
              }
              onChange={onChangeMethod}
              className={
                newTestLearnConfig.setting.method !==
                testLearningConfig.setting.method
                  ? "new-dep-select edited"
                  : "new-dep-select"
              }
            >
              {methods.map(item => {
                return <option>{item}</option>;
              })}
            </select>
          </div>
          <div className="new-dep-container-select">
            <p className="new-dep-p">Split Mechanism: </p>
            <select
              value={newTestLearnConfig.setting.split_mechanism}
              onChange={onChangeSplitMechanism}
              className={
                newTestLearnConfig.setting.split_mechanism !==
                testLearningConfig.setting.split_mechanism
                  ? "new-dep-select edited"
                  : "new-dep-select"
              }
            >
              {renderSplitMechanisms()}
            </select>
          </div>
          <div className="new-dep-container-select">
            <p className="new-dep-p">Feedback Cycle: </p>
            <select
              value={newTestLearnConfig.setting.feedback_cycle}
              onChange={onChangeFeedbackCycle}
              className={
                newTestLearnConfig.setting.feedback_cycle !==
                testLearningConfig.setting.feedback_cycle
                  ? "new-dep-select edited"
                  : "new-dep-select"
              }
            >
              {feedbackCycles.map(item => {
                return <option>{item}</option>;
              })}
            </select>
          </div>
          <div className="new-dep-container-inline">
            <div className="new-dep-container-select">
              <p className="new-dep-p">Hold out period: </p>
              <select
                value={newTestLearnConfig.setting.hold_out_period_unit}
                onChange={onChangePeriodUnit}
                className={
                  newTestLearnConfig.setting.hold_out_period_unit !==
                  testLearningConfig.setting.hold_out_period_unit
                    ? "new-dep-select edited"
                    : "new-dep-select"
                }
              >
                {periodUnits.map(item => {
                  return <option>{item}</option>;
                })}
              </select>
              <input
                value={newTestLearnConfig.setting.hold_out_period_length}
                onChange={onChangePeriodLength}
                className={
                  newTestLearnConfig.setting.hold_out_period_length !==
                  testLearningConfig.setting.hold_out_period_length
                    ? "new-dep-input edited"
                    : "new-dep-input"
                }
              />
            </div>
          </div>
          <div className="new-dep-container-button">
            <button
              type="button"
              onClick={onClickCancel}
              className="b--secondary red"
            >
              <div className="close" />
            </button>
            <button
              type="button"
              onClick={onClickSave}
              className="b--secondary green"
            >
              <i className="checkmark" />
            </button>
          </div>
          <div className="new-dep-container-button">
            {errorManager !== "" && <p className="error">{errorManager}</p>}
          </div>
        </div>
      </div>
      <div
        className={
          predictors.length <= 2
            ? predictors.length <= 1
              ? "connecting-line just-one"
              : "connecting-line less-amount"
            : "connecting-line"
        }
      />
      <div className="container-predictors">
        <div className="container-buttons-pred-chart">
          <div className="container-pred-label">
            <button
              type="button"
              onClick={onClickSaveProportions}
              disabled={newTestLearnConfig.setting.method !== "Define Manually"}
              className={
                newTestLearnConfig.setting.method !== "Define Manually"
                  ? "b--secondary green disabled"
                  : "b--secondary green"
              }
            >
              <i className="checkmark" />
            </button>
            <button
              type="button"
              onClick={onClickAddPredictor}
              className="b--mat b--affirmative text-upper button-add-pred"
            >
              <i className="plus-button" />
              add predictor
            </button>
            <p className="label-pred">
              # of predictors: {newPredictors.length}
            </p>
          </div>

          <button
            type="button"
            onClick={onClickShowChart}
            className="b--mat b--affirmative text-upper button-show-chart"
          >
            <div className="i--icon-chart" />
          </button>
        </div>
        {errorProportions !== "" && (
          <p className="error sum-error">{errorProportions}</p>
        )}
        {messageProportions !== "" && <p>{messageProportions}</p>}
        <div>
          {newPredictors.length === 0 ? (
            <p className="label-no-pred">
              Currently you have no predictors setup to run inference on.
              <br />
              Add one or more predictors to run your deployment pipeline.
            </p>
          ) : (
            <div className="container-rows">{renderPredictors()}</div>
          )}
        </div>
      </div>
      <Modal
        isOpen={openAddPredictor}
        toggle={onClickCloseAddPredictor}
        className={"add-predictor-modal-container"}
      >
        <ModalBody>
          <AddPredictor
            splitMechanism={newTestLearnConfig.setting.split_mechanism}
            onClose={onClickCloseAddPredictor}
            reload={reload}
          />
        </ModalBody>
      </Modal>
      <Modal
        isOpen={openChart}
        toggle={onClickCloseChart}
        className={"chart-modal-container"}
      >
        <ModalBody>
          <PredictorChart />
        </ModalBody>
      </Modal>
    </div>
  );
};

NewDeploymentPage.propTypes = {
  tab: PropTypes.string
};

NewDeploymentPage.defaultProps = {
  tab: "Deployment"
};

export default withRouter(NewDeploymentPage);
