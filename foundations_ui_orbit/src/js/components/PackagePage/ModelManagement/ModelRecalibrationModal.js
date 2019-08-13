import React, { Component } from "react";
import PropTypes from "prop-types";
import { Modal, ModalBody } from "reactstrap";
import Papa from "papaparse";
import TrainingDateRow from "./TrainingDateRow";
import MultiSelect from "@kenshooui/react-multi-select";
import "@kenshooui/react-multi-select/dist/style.css";
import BaseActions from "../../../actions/BaseActions";

class ModelRecalibrationModal extends Component {
  constructor(props) {
    super(props);
    this.clickSchedule = this.clickSchedule.bind(this);
    this.clickSwap = this.clickSwap.bind(this);
    this.clickTriggered = this.clickTriggered.bind(this);
    this.clickFrequency = this.clickFrequency.bind(this);
    this.clickTime = this.clickTime.bind(this);
    this.getData = this.getData.bind(this);
    this.addDate = this.addDate.bind(this);
    this.removeDate = this.removeDate.bind(this);
    this.formatPopulationData = this.formatPopulationData.bind(this);
    this.changePopulation = this.changePopulation.bind(this);
    this.saveChanges = this.saveChanges.bind(this);
    this.state = {
      closeModal: this.props.closeModal,
      modelName: this.props.modelName,
      isShowingScheduleMessage: false,
      isShowingSwapMessage: false,
      isShowingTriggeredMessage: false,
      isShowingFrequencyMessage: false,
      isShowingTimeMessage: false,
      trainingDates: [],
      trainingDateItems: [],
      populationItems: [],
      selectedPopulationItems: [],
      isLoading: false,
      isComplete: false
    };
  }

  componentWillMount() {
    BaseActions.getFromApiary("dates/target").then(result => {
      if (result) {
        this.getData(result);
        this.formatPopulationData();
      }
    });
  }

  clickSchedule() {
    const { isShowingScheduleMessage } = this.state;
    this.setState({ isShowingScheduleMessage: !isShowingScheduleMessage });
  }

  clickSwap() {
    const { isShowingSwapMessage } = this.state;
    this.setState({ isShowingSwapMessage: !isShowingSwapMessage });
  }

  clickTriggered() {
    const { isShowingTriggeredMessage } = this.state;
    this.setState({ isShowingTriggeredMessage: !isShowingTriggeredMessage });
  }

  clickFrequency() {
    const { isShowingFrequencyMessage } = this.state;
    this.setState({ isShowingFrequencyMessage: !isShowingFrequencyMessage });
  }

  clickTime() {
    const { isShowingTimeMessage } = this.state;
    this.setState({ isShowingTimeMessage: !isShowingTimeMessage });
  }

  getData(result) {
    result.data.sort(function(a, b) {
      let dateA = new Date(a),
        dateB = new Date(b);
      return dateA - dateB;
    });
    result.data.reverse();

    this.setState({ trainingDates: result.data });
  }

  addDate(selectedItem) {
    const { trainingDates, trainingDateItems } = this.state;

    const selectedDate = selectedItem[0];
    const updatedTrainingDateItems = trainingDateItems.filter(row => {
      return row != selectedDate;
    });
    let updatedTrainingDates = JSON.parse(JSON.stringify(trainingDates));
    updatedTrainingDates.push([selectedDate.label]);

    updatedTrainingDates.sort(function(a, b) {
      let dateA = new Date(a),
        dateB = new Date(b);
      return dateA - dateB;
    });

    updatedTrainingDates.reverse();

    this.setState({
      trainingDates: updatedTrainingDates,
      trainingDateItems: updatedTrainingDateItems
    });
  }

  removeDate(date) {
    const { trainingDates, trainingDateItems } = this.state;

    const updatedTrainingDates = trainingDates.filter(row => {
      return row != date;
    });

    let updatedTrainingDateItems = JSON.parse(
      JSON.stringify(trainingDateItems)
    );

    let index = 0;
    if (updatedTrainingDateItems.length > 0) {
      index = trainingDateItems[trainingDateItems.length - 1].id;
    }

    updatedTrainingDateItems.push({ id: index, label: date });

    updatedTrainingDateItems.sort(function(a, b) {
      let dateA = new Date(a.label),
        dateB = new Date(b.label);
      return dateA - dateB;
    });

    updatedTrainingDateItems.reverse();

    this.setState({
      trainingDates: updatedTrainingDates,
      trainingDateItems: updatedTrainingDateItems
    });
  }

  formatPopulationData() {
    BaseActions.getFromApiary("populations").then(result => {
      let populationRows = [];
      let index = 0;
      if (result) {
        result.data.forEach(pop => {
          const label = "Name: " + pop.name + ", Status: " + pop.status;
          populationRows.push({ id: index, label: label });
          index++;
        });
      }

      this.setState({ populationItems: populationRows });
    });
  }

  changePopulation(selectedItems) {
    this.setState({ selectedPopulationItems: selectedItems });
  }

  saveChanges() {
    const { selectedPopulationItems, trainingDates } = this.state;

    this.setState({ isLoading: true });

    const finalData =
      '{"TrainPopulations": ' +
      JSON.stringify(selectedPopulationItems) +
      ', "TrainDateTimes": [' +
      trainingDates.map(item => '"' + item[0] + '"') +
      "]}";

    BaseActions.postJSONFile(
      "files/recalibrate",
      "config.json",
      finalData
    ).then(result => {
      this.setState({ isLoading: false, isComplete: true });
    });
  }

  render() {
    const {
      closeModal,
      modelName,
      isShowingScheduleMessage,
      isShowingSwapMessage,
      isShowingTriggeredMessage,
      isShowingFrequencyMessage,
      isShowingTimeMessage,
      trainingDates,
      trainingDateItems,
      populationItems,
      selectedPopulationItems,
      isLoading,
      isComplete
    } = this.state;

    let scheduleMessage = null;
    if (isShowingScheduleMessage) {
      scheduleMessage = (
        <p className="checkbox-text error-message">
          Configuring in GUI is not supported yet
        </p>
      );
    }

    let swapMessage = null;
    if (isShowingSwapMessage) {
      swapMessage = (
        <p className="checkbox-text error-message">
          Configuring in GUI is not supported yet
        </p>
      );
    }

    let triggeredMessage = null;
    if (isShowingTriggeredMessage) {
      triggeredMessage = (
        <p className="checkbox-text error-message">
          Configuring in GUI is not supported yet
        </p>
      );
    }

    let frequencyMessage = null;
    if (isShowingFrequencyMessage) {
      frequencyMessage = (
        <p className="checkbox-text error-message">
          Configuring in GUI is not supported yet
        </p>
      );
    }

    let timeMessage = null;
    if (isShowingTimeMessage) {
      timeMessage = (
        <p className="checkbox-text error-message">
          Configuring in GUI is not supported yet
        </p>
      );
    }

    let trainingDateRows = [];
    trainingDates.forEach(date => {
      trainingDateRows.push(
        <TrainingDateRow key={date} date={date} removeDate={this.removeDate} />
      );
    });

    let buttonDiv = (
      <div className="manage-inference-modal-button-container">
        <button
          type="button"
          onClick={closeModal}
          className="b--mat b--negation text-upper"
        >
          cancel changes
        </button>
        <button
          type="button"
          onClick={this.saveChanges}
          className="b--mat b--affirmative text-upper"
        >
          Run Recalibration
        </button>
      </div>
    );

    if (isLoading) {
      buttonDiv = (
        <div className="manage-inference-modal-button-container">
          <button
            type="button"
            onClick={closeModal}
            className="b--mat b--negation text-upper"
            disabled
          >
            Recalibrating
          </button>
        </div>
      );
    } else if (isComplete) {
      buttonDiv = (
        <div className="manage-inference-modal-button-container">
          <button
            type="button"
            onClick={closeModal}
            className="b--mat b--affirmative text-upper"
          >
            Completed, Close Modal
          </button>
        </div>
      );
    }

    return (
      <Modal
        isOpen={true}
        toggle={closeModal}
        className={"model-recalibration-modal-container"}
      >
        <ModalBody>
          <div>
            <div className="model-recalibration-upper">
              <p className="model-recalibration-modal-header font-bold text-upper">
                Modal Recalibration
              </p>
              <p className="model-recalibration-model-name font-bold">
                {modelName}
              </p>
              <p>Define the frequency at which models are re-trained:</p>
              <div className="checkbox-div">
                <label className="font-bold">
                  <input
                    name="Schedule"
                    type="checkbox"
                    className="checkbox-label"
                    onClick={this.clickSchedule}
                    defaultChecked={false}
                  />
                  Schedule
                </label>
                {scheduleMessage}
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
                    onClick={this.clickSwap}
                    defaultChecked={false}
                  />
                  Auto-Swap
                </label>
                {swapMessage}
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
                    onClick={this.clickTriggered}
                    defaultChecked={false}
                  />
                  Triggered
                </label>
                {triggeredMessage}
                <p className="checkbox-text">
                  Turning this one will automatically retrain model when key
                  model performance metrics decline over 15%
                </p>
              </div>
              <div className="frequency-time-container">
                <p className="frequency-text">Frequency:</p>
                <div
                  className="frequency-container disabled"
                  onClick={this.clickFrequency}
                >
                  <div className="i--icon-edit-container">
                    <div className="i--icon-edit" role="presentation" />
                  </div>
                </div>
                {frequencyMessage}
              </div>
              <div className="frequency-time-container">
                <p className="frequency-text">Start Time:</p>
                <div
                  className="frequency-container disabled"
                  onClick={this.clickTime}
                >
                  <div className="i--icon-cal-clock-container">
                    <div className="i--icon-cal-clock" role="presentation" />
                  </div>
                </div>
                {timeMessage}
              </div>
            </div>
            <div className="model-recalibration-lower">
              <div className="training-data-select-container">
                <div className="training-data-container">
                  <div className="training-data-header">
                    <p className="font-bold">Training Data</p>
                  </div>
                  <div className="training-rows">{trainingDateRows}</div>
                </div>
                <div className="training-data-container multi-select-container">
                  <div className="add-training-data-header">
                    <p className="font-bold">Add Training Data</p>
                  </div>
                  <MultiSelect
                    items={trainingDateItems}
                    selectedItems={[]}
                    onChange={this.addDate}
                    showSearch={false}
                    showSelectAll={false}
                    showSelectedItems={false}
                    wrapperClassName={"multi-select"}
                  />
                </div>
              </div>
              <div className="population-select-container multi-select-container">
                <div className="add-training-data-header">
                  <p className="font-bold aligned">Select Populations</p>
                </div>
                <MultiSelect
                  items={populationItems}
                  selectedItems={selectedPopulationItems}
                  onChange={this.changePopulation}
                  showSearch={false}
                  showSelectAll={false}
                  showSelectedItems={false}
                  wrapperClassName={"multi-select"}
                />
                <p>
                  Using default training/validation data split configuration.
                  This can be configured in config.json
                </p>
              </div>
            </div>
            {buttonDiv}
          </div>
        </ModalBody>
      </Modal>
    );
  }
}
ModelRecalibrationModal.propTypes = {
  closeModal: PropTypes.func,
  modelName: PropTypes.string,
  isShowingScheduleMessage: PropTypes.bool,
  isShowingSwapMessage: PropTypes.bool,
  isShowingTriggeredMessage: PropTypes.bool,
  isShowingFrequencyMessage: PropTypes.bool,
  isShowingTimeMessage: PropTypes.bool,
  trainingDates: PropTypes.array,
  trainingDateItems: PropTypes.array,
  populationItems: PropTypes.array,
  selectedPopulationItems: PropTypes.array,
  isLoading: PropTypes.bool,
  isComplete: PropTypes.bool
};

ModelRecalibrationModal.defaultProps = {
  closeModal: () => {},
  modelName: "",
  isShowingScheduleMessage: false,
  isShowingSwapMessage: false,
  isShowingTriggeredMessage: false,
  isShowingFrequencyMessage: false,
  isShowingTimeMessage: false,
  trainingDates: [],
  trainingDateItems: [],
  populationItems: [],
  selectedPopulationItems: [],
  isLoading: false,
  isComplete: false
};
export default ModelRecalibrationModal;
