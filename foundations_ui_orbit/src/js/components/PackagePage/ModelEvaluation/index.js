import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";
import Preview from "./Preview";
import Loading from "../../common/Loading";
import Schedule from "./Schedule";

const ModelEvaluation = props => {
  const [dates, setDates] = React.useState([]);
  const [selectedDates, setSelectedDates] = React.useState([]);
  const [loadingEval, setLoadingEval] = React.useState(true);
  const [loading, setLoading] = React.useState(false);
  const [evaluations, setEvaluations] = React.useState([]);
  const [firstReload, setFirstReload] = React.useState(true);

  const reload = () => {
    setLoadingEval(true);

    BaseActions.getFromApiary(
      "projects/" + props.location.state.project.name + "/metrics"
    ).then(result => {
      if (result) {
        setEvaluations(result);
        setLoadingEval(false);
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onChangeDate = date => {
    let foundValue = selectedDates.includes(date);

    setSelectedDates(prevSelectedDates =>
      foundValue === false
        ? [...prevSelectedDates, date]
        : prevSelectedDates.filter(
            prevSelectedDate => prevSelectedDate.value !== date.value
          )
    );
  };

  const onClickLoadResults = () => {
    setLoading(true);
    const eval_period_datetimes = selectedDates.map(date => {
      return date.value;
    });

    let data = {
      eval_period_datetimes: eval_period_datetimes
    };

    const body = JSON.stringify(data);

    BaseActions.postJSONFile("files/performance", "config.json", body)
      .then(response => {
        setLoading(false);
        reload();
      })
      .catch(e => {
        setLoading(false);
      });
  };
  return (
    <Layout tab={props.tab} title="Model Evaluation">
      <Schedule />
      {loadingEval === false ? (
        <div className="container-evaluation">
          <div className="container-top-section">
            <div className="container-num-metrics">
              <p>
                <span>NUMBER OF DASHBOARD METRICS: {evaluations.length}</span>
              </p>
            </div>
          </div>
          {evaluations.length > 0 ? (
            <div className="container-eval-content">
              {evaluations.map((evaluation, i) => {
                return <Preview evaluation={evaluation} />;
              })}
            </div>
          ) : (
            <div className="container-eval-empty">
              <p>It's a fresh start.</p>
              <p>There are currently no metrics to look at.</p>
            </div>
          )}
        </div>
      ) : (
        <Loading loadingMessage="We are currently loading your evaluations" />
      )}
    </Layout>
  );
};

ModelEvaluation.propTypes = {
  tab: PropTypes.string
};

ModelEvaluation.defaultProps = {
  tab: "Evaluation"
};

export default withRouter(ModelEvaluation);
