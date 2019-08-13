import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PredictorRow from "./PredictorRow.js";
import BaseActions from "../../../actions/BaseActions.js";

const Predictors = props => {
  const [error, setError] = React.useState("");
  const [message, setMessage] = React.useState("");

  const onClickAddPredictor = () => {
    props.onClickAddPredictor();
  };

  const onClickShowChart = () => {
    props.onClickShowChart();
  };

  const onClickSaveProportions = () => {
    setError("");
    setMessage("");
    let result = 0;
    props.predictors.forEach(item => {
      result += item.proportion;
    });

    if (result !== 1) {
      setError(
        "Please make sure that the sum of all proportions is equal to 1 (100%)"
      );
    } else {
      let data = props.predictors.map(item => {
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
        props.reload();
        setMessage("Changes saved!");
      });
    }
  };

  const renderPredictors = () => {
    let proportion = 0;
    let predictors_count = props.predictors.length;

    return props.predictors.map(predictor => {
      if (props.method === "Define Manually") {
        if (predictors_count === 1) {
          proportion = 1;
        } else if (predictors_count > 1) {
          const filteredPopulations = props.testLearningConfig.populations.filter(
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
          predictors={props.predictors}
          proportion={proportion}
          changeProportion={value =>
            props.onChangeSingleProportion(predictor, value)
          }
          method={props.method}
          splitMechanism={props.splitMechanism}
          reload={props.reload}
        />
      );
    });
  };

  return (
    <div className="container-predictors">
      <div className="container-buttons-pred-chart">
        <div className="container-pred-label">
          <button
            type="button"
            onClick={onClickSaveProportions}
            disabled={props.method !== "Define Manually"}
            className={
              props.method !== "Define Manually"
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
            # of predictors: {props.predictors.length}
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
        {props.predictors.length === 0 ? (
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
  onChangePredictorsProportions: PropTypes.func,
  onChangeSingleProportion: PropTypes.func,
  onClickShowChart: PropTypes.func,
  splitMechanism: PropTypes.string,
  reload: PropTypes.func
};

Predictors.defaultProps = {
  predictors: [],
  method: "Define Manually",
  splitMechanism: "spec"
};

export default withRouter(Predictors);
