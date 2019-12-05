import React from "react";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Flatpickr from "react-flatpickr";
import Select from "react-select";
import { get, postJSONFile } from "../../../actions/BaseActions";

const Schedule = () => {
  const [scheduleData, setScheduleData] = React.useState({
    start_datetime: "",
    end_datetime: "",
    frequency: ""
  });
  const [open, setOpen] = React.useState(false);
  const [error, setError] = React.useState("");
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const options = [
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
  ];
  const [selectedOption, setSelectedOption] = React.useState("");
  const pickerStartDateRef = React.useRef();
  const pickerEndDateRef = React.useRef();
  const [message, setMessage] = React.useState("");
  const [dates, setDates] = React.useState([]);
  const [selectedDate, setSelectedDate] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const reload = () => {
    get("dates/inference").then(result => {
      if (result) {
        const items = [];

        if (result.data.length > 0) {
          result.data.forEach(item => {
            items.push({
              label: item,
              value: item
            });
          });

          const sortedItems = items.sort((a, b) => {
            const date1 = new Date(a.value);
            const date2 = new Date(b.value);
            return date2 - date1;
          });
          setDates(sortedItems);
          setSelectedDate(sortedItems[0].value);
        } else {
          result.meta.fields.forEach(value => {
            items.push({
              label: value,
              value: value
            });
          });
          setDates(items);
          setSelectedDate(items[0].value);
        }
      }

      get("schedule").then(resultSchedule => {
        if (
          resultSchedule
          && resultSchedule.data
          && resultSchedule.data.start_datetime
          && resultSchedule.data.end_datetime
          && resultSchedule.data.frequency
        ) {
          const startDateTime = resultSchedule.data.start_datetime
            ? new Date(resultSchedule.data.start_datetime)
            : "";

          const endDateTime = resultSchedule.data.end_datetime
            ? new Date(resultSchedule.data.end_datetime)
            : "";

          const freq = resultSchedule.data.frequency
            ? {
              label: resultSchedule.data.frequency,
              value: resultSchedule.data.frequency
            }
            : "";

          setScheduleData(resultSchedule.data);
          setStartDate(startDateTime);
          setEndDate(endDateTime);
          setSelectedOption(freq);
        }
      });
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
    const data = {
      start_datetime: startDate.toString(),
      end_datetime: endDate.toString(),
      frequency: selectedOption.value
    };

    postJSONFile("schedule", "inference_schedule.json", data).then(() => {
      setMessage(
        "Schedule has been saved. Inference will be executed at scheduled time"
      );
      reload();
    });
  };

  const onClickCancelSchedule = () => {
    const startValue = scheduleData.start_datetime
      ? new Date(scheduleData.start_datetime)
      : "";

    const endValue = scheduleData.end_datetime
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

  const onClickRunInference = () => {
    setLoading(true);

    get("learn").then(result => {
      if (result.data.setting && result.data.populations) {
        get("predictors").then(resultPredictors => {
          if (resultPredictors.data) {
            let values = resultPredictors.data;
            if (values.length === 1) {
              values[0].proportion = 1;
            } else if (values.length > 1) {
              const newPredictors = values.map(predictor => {
                const newPredictor = predictor;
                const filteredPopulations = result.data.populations.filter(
                  item => item.name === newPredictor.name
                );
                if (filteredPopulations.length >= 1) {
                  newPredictor.proportion = filteredPopulations[0].proportion;
                }
                return newPredictor;
              });

              values = newPredictors;
            }

            const data = {
              inference_period_datetime: selectedDate,
              population_setup_period_datetime: selectedDate,
              populations: values
            };

            const finalData = JSON.stringify(data);

            postJSONFile("files/run", "config.json", finalData)
              .then(() => {
                setLoading(false);
                setOpen(false);
                reload();
              })
              .catch(() => {
                setLoading(false);
                setError(
                  "There was a problem running the inference. Please try again"
                );
              });
          }
        });
      }
    });
  };
  return (
    <div className="scheduling-container">
      <p className="new-dep-section font-bold">SCHEDULING</p>
      <p>{message}</p>
      <div className="manual-schedule-container">
        <p className="subheader">Manual</p>
        <button
          type="button"
          onClick={onClickOpenInferenceModal}
          className="b--mat b--affirmative text-upper new-dep-button"
        >
          {loading === true ? "running" : "run inference now"}
        </button>
      </div>

      <div className="container-scheduling">
        <div className="container-schedule-date">
          <p className="subheader">AUTOMATED</p>
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
                selectedOption !== ""
                && selectedOption.value !== scheduleData.frequency
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
      <Modal
        isOpen={open}
        toggle={onClickCloseInferenceModal}
        className="manage-inference-modal-container"
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
                  return <option key={date.value}>{date.value}</option>;
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
      </Modal>
    </div>
  );
};

Schedule.propTypes = {};

Schedule.defaultProps = {};

export default withRouter(Schedule);
