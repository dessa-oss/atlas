import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Flatpickr from "react-flatpickr";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";

const Schedule = props => {
  const [scheduleData, setScheduleData] = React.useState({
    start_datetime: "",
    end_datetime: "",
    frequency: ""
  });
  const [open, setOpen] = React.useState(false);
  const [error, setError] = React.useState("");
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const [options, setOptions] = React.useState([
    {
      label: "Hourly",
      value: "Hourly"
    },
    {
      label: "Daily",
      value: "Daily"
    },
    {
      label: "Weekly",
      value: "Weekly"
    },
    {
      label: "Bi-Weekly",
      value: "Bi-Weekly"
    },
    {
      label: "Monthly",
      value: "Monthly"
    },
    {
      label: "Quaterly",
      value: "Quaterly"
    },
    {
      label: "Semi-Annually",
      value: "Semi-Annually"
    }
  ]);
  const [selectedOption, setSelectedOption] = React.useState("");
  const pickerStartDateRef = React.useRef();
  const pickerEndDateRef = React.useRef();
  const [message, setMessage] = React.useState("");
  const [dates, setDates] = React.useState([]);
  const [selectedDate, setSelectedDate] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const reload = () => {
    BaseActions.getFromApiary(
      "/projects/" + props.location.state.project.name + "/evaluation_schedule"
    ).then(resultSchedule => {
      if (
        resultSchedule &&
        resultSchedule.schedule &&
        resultSchedule.schedule.start_datetime &&
        resultSchedule.schedule.end_datetime &&
        resultSchedule.schedule.frequency
      ) {
        let start_datetime = resultSchedule.schedule.start_datetime
          ? new Date(resultSchedule.schedule.start_datetime)
          : "";

        let end_datetime = resultSchedule.schedule.end_datetime
          ? new Date(resultSchedule.schedule.end_datetime)
          : "";

        let freq = resultSchedule.schedule.frequency
          ? {
              label: resultSchedule.schedule.frequency,
              value: resultSchedule.schedule.frequency
            }
          : "";

        setScheduleData(resultSchedule.schedule);
        setStartDate(start_datetime);
        setEndDate(end_datetime);
        setSelectedOption(freq);
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onChangeStartDate = date => {
    setStartDate(date);
  };

  const onChangeEndDate = date => {
    setEndDate(date);
  };

  const onClickOpenStartDate = () => {
    pickerStartDateRef.current.flatpickr.open();
  };

  const onClickOpenEndDate = () => {
    pickerEndDateRef.current.flatpickr.open();
  };

  const onChangeOption = option => {
    setSelectedOption(option);
  };

  const onChangeInferenceDate = e => {
    setSelectedDate(e.target.value);
  };

  const onClickSaveSchedule = () => {
    setMessage("");
    let data = {
      schedule: {
        start_datetime: startDate.toString(),
        end_datetime: endDate.toString(),
        frequency: selectedOption.value
      }
    };

    BaseActions.putApiary(
      "/projects/" + props.location.state.project.name + "/evaluation_schedule",
      data
    ).then(() => {
      setMessage(
        "Schedule has been saved. Inference will be executed at scheduled time"
      );
      reload();
    });
  };

  const onClickCancelSchedule = () => {
    let startValue = scheduleData.start_datetime
      ? new Date(scheduleData.start_datetime)
      : "";

    let endValue = scheduleData.end_datetime
      ? new Date(scheduleData.end_datetime)
      : "";

    let frequencyValue = "";

    if (scheduleData.frequency) {
      frequencyValue = {
        label: scheduleData.frequency,
        value: scheduleData.frequency
      };
    }

    setStartDate(startValue);
    setEndDate(endValue);
    setSelectedOption(frequencyValue);
  };

  const onClickOpenInferenceModal = () => {
    setOpen(true);
  };

  const onClickCloseInferenceModal = () => {
    setOpen(false);
  };

  const onClickAutoRunInference = () => {
    setLoading(true);
    setError("");
    BaseActions.postJSONFile("files/run/auto", "config.json", {})
      .then(() => {
        setLoading(false);
        setOpen(false);
        reload();
      })
      .catch(error => {
        setLoading(false);
        setError("There was a problem running the inference. Please try again");
      });
  };

  return (
    <div className="scheduling-container">
      <p className="new-dep-section font-bold">SCHEDULING</p>
      <p>{message}</p>

      <div className="container-scheduling">
        <div className="container-schedule-date">
          <p class="subheader">AUTOMATED</p>
          <p className="label-date">Start: </p>
          <div className="container-date">
            <Flatpickr
              placeholder="Select Start Date"
              value={startDate}
              ref={pickerStartDateRef}
              onChange={onChangeStartDate}
            />
          </div>
          <div className="container-icon-date" onClick={onClickOpenStartDate}>
            <div className="icon-date" role="presentation" />
          </div>
        </div>
        <div className="container-schedule-date">
          <p className="label-date">End: </p>
          <div className="container-date">
            <Flatpickr
              placeholder="Select End Date"
              value={endDate}
              ref={pickerEndDateRef}
              onChange={onChangeEndDate}
            />
          </div>
          <div className="container-icon-date" onClick={onClickOpenEndDate}>
            <div className="icon-date" role="presentation" />
          </div>
        </div>
        <div className="container-schedule-date">
          <p className="label-date">Frequency: </p>
          <div className="container-date">
            <Select
              className={
                selectedOption !== "" &&
                selectedOption.value !== scheduleData.frequency
                  ? "select-frequency adaptive edited"
                  : "select-frequency adaptive"
              }
              value={selectedOption}
              onChange={onChangeOption}
              options={options}
            />
          </div>
        </div>
        <div className="container-buttons-scheduling">
          <button
            type="button"
            onClick={onClickSaveSchedule}
            className="b--secondary green"
          >
            <i className="checkmark" />
          </button>
          <button
            type="button"
            onClick={onClickCancelSchedule}
            className="b--secondary red"
          >
            <div className="close" />
          </button>
        </div>
      </div>
      {/* <Modal
        isOpen={open}
        toggle={onClickCloseInferenceModal}
        className={"manage-inference-modal-container"}
      >
        <ModalBody>
          <div>
            <p className="manage-inference-modal-header font-bold text-upper">
              Selecting inference date
            </p>
            <div className="manage-interface-property-container">
              <p className="manage-interface-modal-label">Inference Date:</p>
              <select
                className="manage-interface-modal-select"
                onChange={onChangeInferenceDate}
              >
                {dates.map(date => {
                  return <option>{date.value}</option>;
                })}
              </select>
            </div>
            <div className="manage-inference-modal-button-container">
              <button
                type="button"
                onClick={onClickCloseInferenceModal}
                className="b--mat b--negation text-upper"
              >
                cancel
              </button>
              <button
                type="button"
                onClick={onClickRunInference}
                className="b--mat b--affirmative text-upper"
              >
                {loading === true ? "running" : "run"}
              </button>
            </div>
            {error !== "" && <p>{error}</p>}
          </div>
        </ModalBody>
      </Modal> */}
    </div>
  );
};

Schedule.propTypes = {};

Schedule.defaultProps = {};

export default withRouter(Schedule);
