import React from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { getFromApiary } from "../../../actions/BaseActions";
import Preview from "./Preview";
import Loading from "../../common/Loading";
import Schedule from "./Schedule";

const ModelEvaluation = props => {
  const [loadingEval, setLoadingEval] = React.useState(true);
  const [evaluations, setEvaluations] = React.useState([]);

  const reload = () => {
    setLoadingEval(true);

    getFromApiary(
      `projects/${props.location.state.project.name}/metrics`
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

  const { tab } = props;

  return (
    <Layout tab={tab} title="Model Evaluation">
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
              {evaluations.map(evaluation => {
                return <Preview key={evaluation.title.text} evaluation={evaluation} />;
              })}
            </div>
          ) : (
            <div className="container-eval-empty">
              <p>It{"'"}s a fresh start.</p>
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
  tab: PropTypes.string,
  location: PropTypes.object
};

ModelEvaluation.defaultProps = {
  tab: "Evaluation",
  location: { state: {} }
};

export default withRouter(ModelEvaluation);
