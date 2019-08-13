import React from "react";
import Flatpickr from "react-flatpickr";
import PropTypes from "prop-types";
import { Modal, ModalBody } from "reactstrap";
import moment from "moment";
import BaseActions from "../../../actions/BaseActions";

const NewModelRecalibrationModal = props => {
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const start_date_picker_ref = React.createRef();
  const end_date_picker_ref = React.createRef();
  const [modelName, setModelName] = React.useState(props.model.model_name);
  const [error, setError] = React.useState("");

  const onChangeStartDate = e => {
    setStartDate(e[0]);
  };

  const onChangeEndDate = e => {
    setEndDate(e[0]);
  };

  const onChangeModelName = e => {
    setModelName(e.target.value);
  };

  const onClickOpenStartDate = () => {
    start_date_picker_ref.open();
  };

  const onClickOpenEndDate = () => {
    end_date_picker_ref.open();
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
      let body = {
        model_name: modelName,
        start_date: moment(startDate).toString(),
        end_date: moment(endDate).toString()
      };

      BaseActions.postApiary(
        "/projects/" +
          props.location.state.project.name +
          "/" +
          modelName +
          "/retrain",
        body
      ).then(result => {
        props.reload();
        props.onClose();
      });
    }
  };

  return (
    <Modal
      isOpen={true}
      toggle={props.onClose}
      className={"new-model-recalibration-modal-container"}
    >
      <ModalBody>
        <div>
          <p className="manage-inference-modal-header font-bold text-upper">
            Model Recalibration
          </p>
          <div className="recalibrate-property-container">
            <p className="recalibrate-label-date">Start Date: </p>
            <div className="recalibrate-container-date">
              <Flatpickr
                placeholder="Select Start Date"
                value={startDate}
                ref={start_date_picker_ref}
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
                ref={end_date_picker_ref}
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
              className="recalibrate-container-date"
              value={modelName}
              onChange={onChangeModelName}
            />
          </div>
          <div className="manage-inference-modal-button-container">
            <button
              type="button"
              onClick={props.onClose}
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
  model: PropTypes.object,
  reload: PropTypes.func,
  location: PropTypes.object
};

NewModelRecalibrationModal.defaultProps = {};

export default NewModelRecalibrationModal;
