import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Select from "react-select";
import { get, postJSONFile } from "../../../actions/BaseActions";

const EditPredictor = props => {
  const [models, setModels] = React.useState([]);
  const [model, setModel] = React.useState(() => {
    const { predictor } = props;

    return {
      value: predictor.model_package_name,
      label: predictor.model_package_name
    };
  });
  const [actions, setActions] = React.useState([]);
  const [selectedActions, setSelectedActions] = React.useState(() => {
    const { predictor } = props;

    return predictor.action_space.map(item => {
      return {
        value: item,
        label: item
      };
    });
  });
  const [description, setDescription] = React.useState(() => {
    const { predictor } = props;

    return predictor.description;
  });
  const [strategy, setStrategy] = React.useState(() => {
    const { predictor } = props;

    return {
      value: predictor.post_predict_selection.strategy,
      label: predictor.post_predict_selection.strategy
    };
  });
  const [explorationStrategy, setExplorationStrategy] = React.useState(() => {
    const { predictor } = props;

    return {
      value: predictor.post_predict_selection.exploration_strategy,
      label: predictor.post_predict_selection.exploration_strategy
    };
  });
  const [explorationPercentage, setExplorationPercentage] = React.useState(() => {
    const { predictor } = props;

    return predictor.post_predict_selection.exploration_percentage;
  });
  const [environment, setEnvironment] = React.useState(() => {
    const { predictor } = props;
    return {
      value: predictor.environment,
      label: predictor.environment
    };
  });

  const [error, setError] = React.useState("");
  const strategies = [
    {
      value: "uncertainty_with_exploration",
      label: "uncertainty_with_exploration"
    },
    {
      value: "none",
      label: "none"
    }
  ];

  const explorationStrategies = [
    {
      value: "action_counts",
      label: "action_counts"
    },
    {
      value: "ncp",
      label: "ncp"
    },
    {
      value: "none",
      label: "none"
    }
  ];

  const environments = [
    {
      value: "local",
      label: "local"
    }
  ];

  React.useEffect(() => {
    get("management").then(result => {
      const modelsData = [];

      result.data.forEach(item => {
        modelsData.push({
          value: item.model_package_name,
          label: item.model_package_name
        });
      });
      setModels(modelsData);

      get("actions").then(resultActions => {
        const actionsData = [];

        resultActions.data.forEach(item => {
          actionsData.push({
            value: item.name,
            label: item.name
          });
        });
        setActions(actionsData);
      });
    });
  }, []);

  const onChangeModel = value => {
    setModel(value);
  };

  const onChangeActions = action => {
    let insertValue = true;

    selectedActions.forEach(value => {
      if (value.value === action.value) {
        insertValue = false;
      }
    });

    setSelectedActions(prevSelectedActions => (insertValue === true
      ? [...prevSelectedActions, action]
      : prevSelectedActions.filter(
        prevSelectedAction => prevSelectedAction.value !== action.value
      )));
  };

  const onChangeDescription = e => {
    setDescription(e.target.value);
  };

  const onChangeEnvironment = env => {
    setEnvironment(env);
  };

  const onChangeStrategy = value => {
    setStrategy(value);
  };

  const onChangeExplorationStrategy = value => {
    setExplorationStrategy(value);
  };

  const onChangeExplorationPercentage = e => {
    setExplorationPercentage(e.target.value);
  };

  const validateData = () => {
    let message = "";
    let validated = true;

    if (model === ""
      || selectedActions.length === 0
      || description === ""
      || environment === ""
      || strategy === ""
      || explorationStrategy === ""
    ) {
      message = "Error: one or more fields are left empty. Please fill the form.";
      validated = false;
    } else {
      const explorationPercentageValue = parseFloat(explorationPercentage);

      if (
        Number.isNaN(explorationPercentageValue)
        || explorationPercentageValue < 0
        || explorationPercentageValue > 1
      ) {
        message = "Exploration percentage must be a number between 0 and 1";
        validated = false;
      }
    }

    setError(message);
    return validated;
  };

  const onClickSave = () => {
    const {
      splitMechanism, reload, onClose, predictor
    } = props;

    setError("");

    if (validateData()) {
      const explorationPercentageValue = parseFloat(explorationPercentage);

      const newActions = selectedActions.map(item => {
        return item.value;
      });

      const modelValue = model.value;
      const strategyValue = strategy.value;
      const explorationStrategyValue = explorationStrategy.value;
      const environmentValue = environment.value;

      const data = {
        predictor: {
          action_space: newActions,
          description: description,
          model_package_name: modelValue,
          name: predictor.name,
          post_predict_selection: {
            exploration_percentage: explorationPercentageValue,
            exploration_strategy: explorationStrategyValue,
            strategy: strategyValue
          },
          status: "running",
          environment: environmentValue
        },
        split_mechanism: splitMechanism
      };

      postJSONFile(
        "files/predictors/edit",
        "predictors.json",
        data
      ).then(() => {
        reload();
        onClose();
      });
    }
  };

  const { predictor, onClose } = props;

  return (
    <div>
      <p className="manage-inference-modal-header font-bold text-upper">
        Edit predictor {predictor.name}
      </p>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Model:</p>
        <Select
          className="model-performance-select adaptive"
          value={model}
          onChange={onChangeModel}
          options={models}
        />
      </div>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Actions:</p>
        <Select
          className="model-performance-select adaptive"
          value={selectedActions}
          onChange={onChangeActions}
          options={actions}
          closeMenuOnSelect={false}
        />
      </div>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Description:</p>
        <input value={description} onChange={onChangeDescription} />
      </div>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Environment:</p>
        <Select
          className="model-performance-select adaptive"
          value={environment}
          onChange={onChangeEnvironment}
          options={environments}
        />
      </div>
      <p className="manage-inference-modal-subheader font-bold text-upper label-edit-subtitle">
        Post Prediction Selection
      </p>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Strategy:</p>
        <Select
          className="model-performance-select adaptive"
          value={strategy}
          onChange={onChangeStrategy}
          options={strategies}
        />
      </div>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Exploration Strategy:</p>
        <Select
          className="model-performance-select adaptive"
          value={explorationStrategy}
          onChange={onChangeExplorationStrategy}
          options={explorationStrategies}
        />
      </div>
      <div className="manage-interface-property-container">
        <p className="manage-interface-modal-label">Exploration Percentage:</p>
        <input
          value={explorationPercentage}
          onChange={onChangeExplorationPercentage}
        />
      </div>
      <div className="new-dep-container-button">
        <button
          type="button"
          onClick={onClickSave}
          className="b--secondary green"
        >
          <i className="checkmark" />
        </button>
        <button
          type="button"
          onClick={onClose}
          className="b--secondary red"
        >
          <div className="close" />
        </button>
      </div>
      <div className="new-dep-container-button">
        {error !== "" && <p>{error}</p>}
      </div>
    </div>
  );
};

EditPredictor.propTypes = {
  predictor: PropTypes.object,
  onClose: PropTypes.func,
  reload: PropTypes.func,
  splitMechanism: PropTypes.string
};

EditPredictor.defaultProps = {
  predictor: {},
  onClose: () => null,
  reload: () => null,
  splitMechanism: ""

};

export default withRouter(EditPredictor);
