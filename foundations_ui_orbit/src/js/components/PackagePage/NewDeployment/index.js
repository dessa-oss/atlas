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
import Content from "./Content";

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

  const [predictors, setPredictors] = React.useState([]);

  const [method, setMethod] = React.useState("");
  const [splitMechanism, setSplitMechanism] = React.useState("");
  const [openAddPredictor, setOpenAddPredictor] = React.useState(false);
  const [openChart, setOpenChart] = React.useState(false);

  const reload = () => {
    BaseActions.get("learn").then(result => {
      if (result.data.setting && result.data.populations) {
        setTestLearningConfig(result.data);
        setMethod(result.data.setting.method);
        setSplitMechanism(result.data.setting.split_mechanism);

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
          }
        });
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onSetNewMethod = method => {
    setMethod(method);
  };

  const onSetNewSplitMechanism = splitMechanism => {
    setSplitMechanism(splitMechanism);
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

  const onChangeSingleProportion = (predictor, value) => {
    let newPredictors = predictors;
    newPredictors.forEach(item => {
      if (predictor.name === item.name) {
        item.proportion = value;
      }
    });
    setPredictors(newPredictors);
  };

  return (
    <Layout tab={props.tab} title="Deployment">
      <div className="new-dep-container-deployment">
        {/* <Schedule predictors={predictors} /> */}
        <Content />
        <Metadata />
      </div>
    </Layout>
  );
};

NewDeploymentPage.propTypes = {
  tab: PropTypes.string
};

NewDeploymentPage.defaultProps = {
  tab: "Deployment"
};

export default withRouter(NewDeploymentPage);
