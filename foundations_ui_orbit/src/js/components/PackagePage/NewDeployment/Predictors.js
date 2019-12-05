import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PredictorRow from "./PredictorRow";
import { postJSONFile } from "../../../actions/BaseActions";

const Predictors = props => {
  const [error, setError] = React.useState("");
  const [message, setMessage] = React.useState("");

  const onClickSaveProportions = () => {
    const { predictors, reload } = props;

    setError("");
    setMessage("");
    let result = 0;
    predictors.forEach(item => {
      result += item.proportion;
    });

    if (result !== 1) {
      setError(
        "Please make sure that the sum of all proportions is equal to 1 (100%)"
      );
    } else {
      const data = predictors.map(item => {
        return {
          name: item.name,
          proportion: item.proportion
        };
      });

      postJSONFile(
        "files/proportions",
        "test_learn_config.json",
        data
      ).then(() => {
        reload();
        setMessage("Changes saved!");
      });
    }
  };

  const renderPredictors = () => {
    const {
      predictors, method, splitMechanism, reload, onChangeSingleProportion, testLearningConfig
    } = props;

    let proportionValue = 0;
    const predictorsCount = predictors.length;

    return predictors.map(predictor => {
      if (method === "Define Manually") {
        if (predictorsCount === 1) {
          proportionValue = 1;
        } else if (predictorsCount > 1) {
          const filteredPopulations = testLearningConfig.populations.filter(
            item => item.name === predictor.name
          );

          if (filteredPopulations.length >= 1) {
            proportionValue = filteredPopulations[0].proportion;
          }
        }
      }
      return (
        <PredictorRow
          key={predictor.name}
          predictor={predictor}
          predictors={predictors}
          proportion={proportionValue}
          changeProportion={value => onChangeSingleProportion(predictor, value)
          }
          method={method}
          splitMechanism={splitMechanism}
          reload={reload}
        />
      );
    });
  };

  const {
    method, predictors, onClickAddPredictor, onClickShowChart
  } = props;

  return (
    <div className="container-predictors">
      <div className="container-buttons-pred-chart">
        <div className="container-pred-label">
          <button
            type="button"
            onClick={onClickSaveProportions}
            disabled={method !== "Define Manually"}
            className={
              method !== "Define Manually"
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
            # of predictors: {predictors.length}
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
      {error !== "" && <p className="error sum-error">{error}</p>}
      {message !== "" && <p>{message}</p>}
      <div>
        {predictors.length === 0 ? (
          <p className="label-no-pred">
            Current you have no predictors setup to run inference on.
            <br />
            Add one or more predictors to run your deployment pipeline.
          </p>
        ) : (
          <div className="container-rows">{renderPredictors()}</div>
        )}
      </div>
    </div>
  );
};

Predictors.propTypes = {
  testLearningConfig: PropTypes.object,
  predictors: PropTypes.array,
  onClickAddPredictor: PropTypes.func,
  method: PropTypes.string,
  onChangeSingleProportion: PropTypes.func,
  onClickShowChart: PropTypes.func,
  splitMechanism: PropTypes.string,
  reload: PropTypes.func
};

Predictors.defaultProps = {
  predictors: [],
  method: "Define Manually",
  splitMechanism: "spec",
  testLearningConfig: {},
  onClickAddPredictor: () => null,
  onChangeSingleProportion: () => null,
  onClickShowChart: () => null,
  reload: () => null

};

export default withRouter(Predictors);
