import React from "react";
import Flatpickr from "react-flatpickr";
import PropTypes from "prop-types";
import { Modal, ModalBody } from "reactstrap";
import moment from "moment";
import BaseActions from "../../../actions/BaseActions";

class NewModelRecalibrationModal extends React.Component {
  constructor(props) {
    super(props);

    this.onClickOpenStartDate = this.onClickOpenStartDate.bind(this);
    this.onClickOpenEndDate = this.onClickOpenEndDate.bind(this);
    this.onChangeStartDate = this.onChangeStartDate.bind(this);
    this.onChangeEndDate = this.onChangeEndDate.bind(this);
    this.onChangeModelName = this.onChangeModelName.bind(this);
    this.onClickSave = this.onClickSave.bind(this);

    this.state = {
      start_date: "",
      end_date: "",
      start_date_picker_ref: React.createRef(),
      end_date_picker_ref: React.createRef,
      model_name: this.props.model.model_name,
      error: ""
    };
  }

  onChangeStartDate(e) {
    this.setState({
      start_date: e[0]
    });
  }

  onChangeEndDate(e) {
    this.setState({
      end_date: e[0]
    });
  }

  onChangeModelName(e) {
    this.setState({
      model_name: e.target.value
    });
  }

  onClickOpenStartDate() {
    this.state.start_date_picker_ref.open();
  }

  onClickOpenEndDate() {
    this.state.end_date_picker_ref.open();
  }

  onClickSave() {
    this.setState({
      error: ""
    });

    let errorFound = false;

    if (
      this.state.start_date === "" ||
      this.state.end_date === "" ||
      this.state.model_name === ""
    ) {
      errorFound = true;
    }

    if (errorFound === true) {
      this.setState({
        error: "Please fill the form to run the recalibration"
      });
    } else {
      let body = {
        model_name: this.state.model_name,
        start_date: moment(this.state.start_date).toString(),
        end_date: moment(this.state.end_date).toString()
      };

      BaseActions.postApiary(
        "/projects/" +
          this.props.location.state.project.name +
          "/" +
          this.state.model_name +
          "/retrain",
        body
      ).then(result => {
        console.log("RESULT: ", result);
        this.props.reload();
        this.props.onClose();
      });
    }
  }

  render() {
    return (
      <Modal
        isOpen={true}
        toggle={this.props.onClose}
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
                  value={this.state.start_date}
                  ref={this.state.start_date_picker_ref}
                  onChange={this.onChangeStartDate}
                />
              </div>
              <div
                className="container-icon-date"
                onClick={this.onClickOpenStartDate}
              >
                <div className="icon-date" role="presentation" />
              </div>
            </div>
            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">End Date: </p>
              <div className="recalibrate-container-date">
                <Flatpickr
                  placeholder="Select Start Date"
                  value={this.state.end_date}
                  ref={this.state.end_date_picker_ref}
                  onChange={this.onChangeEndDate}
                />
              </div>
              <div
                className="container-icon-date"
                onClick={this.onClickOpenEndDate}
              >
                <div className="icon-date" role="presentation" />
              </div>
            </div>

            <div className="recalibrate-property-container">
              <p className="recalibrate-label-date">Model Name:</p>
              <input className="recalibrate-container-date"
                value={this.state.model_name}
                onChange={this.onChangeModelName}
              />
            </div>
            <div className="manage-inference-modal-button-container">
              <button
                type="button"
                onClick={this.props.onClose}
                className="b--mat b--negation text-upper"
              >
                cancel changes
              </button>
              <button
                type="button"
                onClick={this.onClickSave}
                className="b--mat b--affirmative text-upper"
              >
                Run Recalibration
              </button>
              <div className="new-dep-container-button">
                {this.state.error !== "" && <p>{this.state.error}</p>}
              </div>
            </div>
          </div>
        </ModalBody>
      </Modal>
    );
  }
}

NewModelRecalibrationModal.propTypes = {
  onClose: PropTypes.func,
  model: PropTypes.object,
  reload: PropTypes.func
};

NewModelRecalibrationModal.defaultProps = {};

export default NewModelRecalibrationModal;
