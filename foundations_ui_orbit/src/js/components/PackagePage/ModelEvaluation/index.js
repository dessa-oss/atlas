import React from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { getFromApiary } from "../../../actions/BaseActions";
import Preview from "./Preview";
import Loading from "../../common/Loading";
import Schedule from "./Schedule";
import Charts from "./Charts";

const ModelEvaluation = props => {
  const { tab } = props;

  return (
    <Layout tab={tab} title="Model Evaluation">
      <Schedule />
      <Charts {...props} />
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
