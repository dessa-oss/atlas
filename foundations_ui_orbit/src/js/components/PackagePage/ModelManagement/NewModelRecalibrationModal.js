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

  const onClickSave = () => {
    setError("");

    let errorFound = false;

    if (startDate === "" || endDate === "" || modelName === "") {
      errorFound = true;
    }

    if (errorFound === true) {
      setError("Please fill the form to run the recalibration");
    } else {
      const body = {
        model_name: modelName,
        start_date: moment(startDate).toString(),
        end_date: moment(endDate).toString()
      };

      postApiary(
        `/projects/${
          props.location.state.project.name
        }/${
          modelName
        }/retrain`,
        body
      ).then(() => {
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
            <div className="recalibrate-property-container">
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
            </div>

            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Model Name:</p>
              <input
                className="recalibrate-container-date input"
                value={modelName}
                onChange={onChangeModelName}
                placeholder="Insert Model Name"
              />
            </div>
            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Description:</p>
              <input
                className="recalibrate-container-date input"
                value={description}
                onChange={onChangeDescription}
                placeholder="Insert Description"
              />
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
