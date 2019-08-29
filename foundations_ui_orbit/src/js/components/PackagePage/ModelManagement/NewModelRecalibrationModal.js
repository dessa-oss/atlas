import React from "react";
import Flatpickr from "react-flatpickr";
import PropTypes from "prop-types";
import { Modal, ModalBody } from "reactstrap";
import moment from "moment";
import { postApiary } from "../../../actions/BaseActions";

const NewModelRecalibrationModal = props => {
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const startDatePickerRef = React.createRef();
  const endDatePickerRef = React.createRef();
  const [modelName, setModelName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [scheduleMessageVisible, setScheduleMessageVisible] = React.useState(false);
  const [swapMessageVisible, setSwapMessageVisible] = React.useState(false);
  const [triggeredMessageVisible, setTriggeredMessageVisible] = React.useState(false);
  const [parameters, setParameters] = React.useState([
    {
      key: "",
      value: "",
      placeholder_key: "start_date",
      placeholder_value: "yyyy-mm-dd"
    },
    {
      key: "",
      value: "",
      placeholder_key: "end_date",
      placeholder_value: "yyyy-mm-dd"
    }
  ]);
  const [updatedParameters, setUpdatedParameters] = React.useState([
    {
      key: "",
      value: ""
    },
    {
      key: "",
      value: ""
    }
  ]);

  const [error, setError] = React.useState("");

  const clickSchedule = () => {
    let value = !scheduleMessageVisible;
    setScheduleMessageVisible(value);
  };

  const clickSwap = () => {
    let value = !swapMessageVisible;
    setSwapMessageVisible(value);
  };

  const clickTriggered = () => {
    let value = !triggeredMessageVisible;
    setTriggeredMessageVisible(value);
  };

  const onChangeStartDate = e => {
    setStartDate(e[0]);
  };

  const onChangeEndDate = e => {
    setEndDate(e[0]);
  };

  const onChangeModelName = e => {
    setModelName(e.target.value);
  };

  const onChangeDescription = e => {
    setDescription(e.target.value);
  };

  const onClickOpenStartDate = () => {
    startDatePickerRef.open();
  };

  const onClickOpenEndDate = () => {
    endDatePickerRef.open();
  };

  const onChangeParameterKey = (e, i) => {
    const newParameters = updatedParameters.map((parameter, index) => {
      if (index === i) {
        parameter.key = e.target.value;
      }
      return parameter;
    });

    setUpdatedParameters(updatedParameters);
  };

  const onChangeParameterValue = (e, i) => {
    const newParameters = updatedParameters.map((parameter, index) => {
      if (index === i) {
        parameter.value = e.target.value;
      }
      return parameter;
    });

    setUpdatedParameters(updatedParameters);
  };

  const onClickAddNewParameter = () => {
    const newParameter = {
      key: "",
      value: "",
      placeholder_key: "",
      placeholder_value: ""
    };

    const newUpdatedParameter = {
      key: "",
      value: ""
    };

    setParameters(prevParameters => [...prevParameters, newParameter]);
    setUpdatedParameters(prevUpdatedParameters => [...prevUpdatedParameters, newUpdatedParameter]);
  };


  const onClickSave = () => {
    setError("");

    let errorFound = false;

    if (modelName === "") {
      errorFound = true;
    }

    updatedParameters.forEach(parameter => {
      if (parameter.key === "" || parameter.value === "") {
        errorFound = true;
      }
    });

    if (errorFound === true) {
      setError("Please fill the form to run the recalibration");
    } else {
      let body = {
        model_name: modelName
      };

      updatedParameters.forEach(parameter => {
        body[parameter.key] = parameter.value;
      });

      console.log("BODY: ", body);

      postApiary(`/projects/${props.location.state.project.name}/${modelName}/retrain`,
        body)
        .then(() => {
          props.reload();
          props.onClose();
        });
    }
  };

  const { onClose, model } = props;

  return (
    <Modal
      isOpen
      toggle={onClose}
      className="new-model-recalibration-modal-container"
    >
      <ModalBody>
        <div>
          <p className="manage-inference-modal-header font-bold text-upper">
            Model Recalibration
          </p>
          <p className="model-recalibration-model-name font-bold">
            {model.model_name}
          </p>
          <p>Define the frequency at which models are re-trained:</p>
          <div className="checkbox-div">
            <label className="font-bold">
              <input
                name="Schedule"
                type="checkbox"
                className="checkbox-label"
                onClick={clickSchedule}
                defaultChecked={false}
              />
              Schedule
            </label>
            {scheduleMessageVisible === true && (
              <p className="checkbox-text error-message">
                Not available in this trial
              </p>
            )}
            <p className="checkbox-text">
              Unchecking this will cause your modal retraining to be
              manually triggered
            </p>
          </div>
          <div className="checkbox-div">
            <label className="font-bold">
              <input
                name="Auto-Swap"
                type="checkbox"
                className="checkbox-label"
                onClick={clickSwap}
                defaultChecked={false}
              />
              Auto-Swap
            </label>
            {swapMessageVisible === true && (
              <p className="checkbox-text error-message">
                Not available in this trial
              </p>
            )}
            <p className="checkbox-text">
              Turning this on will automatically deploy model after
              retraining and retire previously active model
            </p>
          </div>
          <div className="checkbox-div">
            <label className="font-bold">
              <input
                name="Triggered"
                type="checkbox"
                className="checkbox-label"
                onClick={clickTriggered}
                defaultChecked={false}
              />
              Triggered
            </label>
            {triggeredMessageVisible === true && (
              <p className="checkbox-text error-message">
                Not available in this trial
              </p>
            )}
            <p className="checkbox-text">
              Turning this one will automatically retrain model when key
              model performance metrics decline over 15%
            </p>
          </div>
          <div className="container-recalibration-properties">
            {/* <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Start Date: </p>
              <div className="recalibrate-container-date">
                <Flatpickr
                  placeholder="Select Start Date"
                  value={startDate}
                  ref={startDatePickerRef}
                  onChange={onChangeStartDate}
                />
              </div>
              <div className="container-icon-date" onClick={onClickOpenStartDate}>
                <div className="icon-date" role="presentation" />
              </div>
            </div>
            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">End Date: </p>
              <div className="recalibrate-container-date">
                <Flatpickr
                  placeholder="Select Start Date"
                  value={endDate}
                  ref={endDatePickerRef}
                  onChange={onChangeEndDate}
                />
              </div>
              <div className="container-icon-date" onClick={onClickOpenEndDate}>
                <div className="icon-date" role="presentation" />
              </div>
            </div> */}

            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Model Name:</p>
              <input
                className="recalibrate-container-date input"
                value={modelName}
                onChange={onChangeModelName}
                placeholder="Enter the name of the new model package (must be unique)"
              />
            </div>
            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Description:</p>
              <input
                className="recalibrate-container-date input"
                value={description}
                onChange={onChangeDescription}
                placeholder="Enter description (optional)"
              />
            </div>
            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date label-parameters">Parameters:</p>
              <div className="table-parameters">
                <div className="container-parameter-row">
                  <div className="parameter"><p className="parameter-header">KEY</p></div>
                  <div className="parameter"><p className="parameter-header">VALUE</p></div>
                </div>
                {
                  parameters.map((parameter, i) => {
                    return (
                      <div key={parameter.key} className="container-parameter-row">
                        <div className="parameter">
                          <input
                            placeholder={parameter.placeholder_key === ""
                              ? "Specify Parameter Key"
                              : parameter.placeholder_key}
                            onChange={e => onChangeParameterKey(e, i)}
                          />
                        </div>
                        <div className="parameter">
                          <input
                            placeholder={parameter.placeholder_value === ""
                              ? "Specify Parameter Value"
                              : parameter.placeholder_value}
                            onChange={e => onChangeParameterValue(e, i)}
                          />
                        </div>
                      </div>
                    );
                  })
                }
                <div className="container-parameter-row">
                  <div className="container-add">
                    <button
                      type="button"
                      onClick={onClickAddNewParameter}
                    >
                      <span>+</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="manage-inference-modal-button-container">
            <button
              type="button"
              onClick={onClose}
              className="b--mat b--negation text-upper"
            >
              cancel changes
            </button>
            <button
              type="button"
              onClick={onClickSave}
              className="b--mat b--affirmative text-upper"
            >
              Run Recalibration
            </button>
            <div className="new-dep-container-button">
              {error !== "" && <p>{error}</p>}
            </div>
          </div>
        </div>
      </ModalBody>
    </Modal>
  );
};

NewModelRecalibrationModal.propTypes = {
  onClose: PropTypes.func,
  reload: PropTypes.func,
  location: PropTypes.object,
  model: PropTypes.object
};

NewModelRecalibrationModal.defaultProps = {
  onClose: () => null,
  reload: () => null,
  location: { state: {} },
  model: {}
};

export default NewModelRecalibrationModal;
