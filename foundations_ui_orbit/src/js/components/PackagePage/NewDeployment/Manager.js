import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import { get, postJSONFile } from "../../../actions/BaseActions";

const Manager = props => {
  const [testLearningConfig, setTestLearningConfig] = React.useState({
    setting: {
      method: "",
      split_mechanism: "",
      feedback_cycle: "",
      hold_out_period_length: "",
      hold_out_period_unit: ""
    }
  });
  const methods = [
    "Define Manually",
    "Automatically Optimize"
  ];
  const [method, setMethod] = React.useState("");

  const [splitMechanisms, setSplitMechanisms] = React.useState([
    "Random split (specified proportion)",
    "Random split (even)"
  ]);

  const [splitMechanism, setSplitMechanism] = React.useState("");

  const feedbackCycles = [
    "Hourly",
    "Daily",
    "Weekly",
    "Bi-Weekly",
    "Monthly",
    "Quaterly",
    "Semy-Annually"
  ];

  const [feedbackCycle, setFeedbackCycle] = React.useState("");
  const [periodLength, setPeriodLength] = React.useState("");
  const periodUnits = [
    "Hour",
    "Day",
    "Week",
    "Month"
  ];
  const [periodUnit, setPeriodUnit] = React.useState("");

  const [error, setError] = React.useState("");

  const loadLearnConfig = () => {
    get("learn").then(result => {
      if (result.data.setting && result.data.populations) {
        setTestLearningConfig(result.data);
        setMethod(result.data.setting.method);
        if (result.data.setting.method === "Define Manually") {
          setSplitMechanisms([
            "Random split (specified proportion)",
            "Random split (even)"
          ]);
        } else if (result.data.setting.method === "Automatically Optimize") {
          setSplitMechanisms(["Multi-arm bandit"]);
        }
        setSplitMechanism(result.data.setting.split_mechanism);
        setFeedbackCycle(result.data.setting.feedback_cycle);
        setPeriodLength(result.data.setting.hold_out_period_length);
        setPeriodUnit(result.data.setting.hold_out_period_unit);

        props.onSetNewSplitMechanism(result.data.setting.split_mechanism);
        props.onSetNewMethod(result.data.setting.method);
      }
    });
  };

  React.useEffect(() => {
    loadLearnConfig();
  }, []);

  const onChangeMethod = e => {
    setMethod(e.target.value);
    props.onSetNewMethod(e.target.value);

    if (e.target.value === "Define Manually") {
      setSplitMechanisms([
        "Random split (specified proportion)",
        "Random split (even)"
      ]);
      setSplitMechanism("Random split (specified proportion)");
      props.onSetNewSplitMechanism("Random split (specified proportion)");
    } else if (e.target.value === "Automatically Optimize") {
      setSplitMechanisms(["Multi-arm bandit"]);
      setSplitMechanism("Multi-arm bandit");
      props.onSetNewSplitMechanism("Random split (specified proportion)");
    }
  };

  const onChangeSplitMechanism = e => {
    setSplitMechanism(e.target.value);
    props.onSetNewSplitMechanism(e.target.value);
  };

  const onChangeFeedbackCycle = e => {
    setFeedbackCycle(e.target.value);
  };

  const onChangePeriodLength = e => {
    setPeriodLength(e.target.value);
  };

  const onChangePeriodUnit = e => {
    setPeriodUnit(e.target.value);
  };

  const validate = () => {
    let validated = true;
    let message = "";

    const periodLengthValue = parseInt(periodLength, 10);

    if (Number.isNaN(periodLengthValue)) {
      validated = false;
      message = "Period length must be an integer";
    }

    setError(message);
    return validated;
  };

  const onClickCancel = () => {
    if (testLearningConfig.setting.method === "Define Manually") {
      setSplitMechanisms([
        "Random split (specified proportion)",
        "Random split (even)"
      ]);
    } else if (testLearningConfig.setting.method === "Automatically Optimize") {
      setSplitMechanisms(["Multi-arm bandit"]);
    }

    setMethod(testLearningConfig.setting.method);
    setSplitMechanism(testLearningConfig.setting.split_mechanism);
    setFeedbackCycle(testLearningConfig.setting.feedback_cycle);
    setPeriodLength(testLearningConfig.setting.hold_out_period_length);
    setPeriodUnit(testLearningConfig.setting.hold_out_period_unit);

    props.onSetNewMethod(testLearningConfig.setting.method);
    props.onSetNewSplitMechanism(testLearningConfig.setting.split_mechanism);
  };

  const onClickSave = () => {
    setError("");

    if (validate()) {
      const periodLengthValue = parseInt(periodLength, 10);

      const data = {
        method: method,
        split_mechanism: splitMechanism,
        feedback_cycle: feedbackCycle,
        hold_out_period_length: periodLengthValue,
        hold_out_period_unit: periodUnit
      };

      postJSONFile("learn", "test_learn_config.json", data).then(
        () => {
          loadLearnConfig();
        }
      );
    }
  };

  return (
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
            value={method}
            onChange={onChangeMethod}
            className={
              method !== testLearningConfig.setting.method
                ? "new-dep-select edited"
                : "new-dep-select"
            }
          >
            {methods.map(item => {
              return <option key={item}>{item}</option>;
            })}
          </select>
        </div>
        <div className="new-dep-container-select">
          <p className="new-dep-p">Split Mechanism: </p>
          <select
            value={splitMechanism}
            onChange={onChangeSplitMechanism}
            className={
              splitMechanism !== testLearningConfig.setting.split_mechanism
                ? "new-dep-select edited"
                : "new-dep-select"
            }
          >
            {splitMechanisms.map(item => {
              return <option key={item}>{item}</option>;
            })}
          </select>
        </div>
        <div className="new-dep-container-select">
          <p className="new-dep-p">Feedback Cycle: </p>
          <select
            value={feedbackCycle}
            onChange={onChangeFeedbackCycle}
            className={
              feedbackCycle !== testLearningConfig.setting.feedback_cycle
                ? "new-dep-select edited"
                : "new-dep-select"
            }
          >
            {feedbackCycles.map(item => {
              return <option key={item}>{item}</option>;
            })}
          </select>
        </div>
        <div className="new-dep-container-inline">
          <div className="new-dep-container-select">
            <p className="new-dep-p">Hold out period: </p>
            <select
              value={periodUnit}
              onChange={onChangePeriodUnit}
              className={
                periodUnit !== testLearningConfig.setting.hold_out_period_unit
                  ? "new-dep-select edited"
                  : "new-dep-select"
              }
            >
              {periodUnits.map(item => {
                return <option key={item}>{item}</option>;
              })}
            </select>
            <input
              className={
                periodLength
                  !== testLearningConfig.setting.hold_out_period_length
                  ? "new-dep-input edited"
                  : "new-dep-input"
              }
              value={periodLength}
              onChange={onChangePeriodLength}
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
          {error !== "" && <p className="error">{error}</p>}
        </div>
      </div>
    </div>
  );
};

Manager.propTypes = {
  onSetNewMethod: PropTypes.func,
  onSetNewSplitMechanism: PropTypes.func
};

Manager.defaultProps = {
  onSetNewMethod: () => null,
  onSetNewSplitMechanism: () => null
};

export default withRouter(Manager);
