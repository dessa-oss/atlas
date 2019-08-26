import React from "react";
import { getFromApiary } from "../../../actions/BaseActions";
import Loading from "../../common/Loading";
import PropTypes from "prop-types";
import Preview from "./Preview";

class Charts extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      evaluations: [],
      loading: false,
      timerId: -1
    };
  }

  setTimer() {
    const value = setInterval(() => {
      getFromApiary(
        `projects/${this.props.location.state.project.name}/metrics`
      ).then(result => {
        if (result) {
          this.setState({
            evaluations: result
          });
        }
      });
    }, 1000);

    this.setState({
      timerId: value
    });
  }

  clearTimer() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  reload() {
    this.setState({
      loading: true
    });

    getFromApiary(
      `projects/${this.props.location.state.project.name}/metrics`
    ).then(result => {
      let newEvaluations = [];
      if (result) {
        newEvaluations = result;
      }
      this.setTimer();

      this.setState({
        evaluations: newEvaluations,
        loading: false
      });
    });
  }

  componentDidMount() {
    this.reload();
  }

  componentWillUnmount() {
    this.clearTimer();
  }

  render() {
    const { evaluations, loading } = this.state;

    if (loading === true) {
      return (
        <Loading loadingMessage="We are currently loading your evaluations" />
      );
    }

    return (
      <div className="container-evaluation">
        <p className="new-dep-section font-bold">MODEL METRICS</p>
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
    );
  }
}

Charts.propTypes = {
  location: PropTypes.object
};

Charts.defaultProps = {
  location: { state: {} }
};

export default Charts;
