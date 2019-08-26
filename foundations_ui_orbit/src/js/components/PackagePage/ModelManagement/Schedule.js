import React from "react";
import { withRouter } from "react-router-dom";
import Flatpickr from "react-flatpickr";
import Select from "react-select";
import { getFromApiary, putApiary } from "../../../actions/BaseActions";
import PropTypes from "prop-types";
import moment from "moment";

const Schedule = props => {
  const [scheduleData, setScheduleData] = React.useState({
    start_datetime: new Date().toString(),
    end_datetime: new Date("2025-01-02").toString(),
    frequency: "Monthly"
  });
  const [startDate, setStartDate] = React.useState(new Date());
  const [endDate, setEndDate] = React.useState(new Date("2025-01-02"));
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
  const [selectedOption, setSelectedOption] = React.useState({
    label: "Monthly",
    value: "Monthly"
  });
  const pickerStartDateRef = React.useRef();
  const pickerEndDateRef = React.useRef();
  const [message, setMessage] = React.useState("");

  const reload = () => {
    getFromApiary(
      `/projects/${props.location.state.project.name}/evaluation_schedule`
    ).then(resultSchedule => {
      // if (
      //   resultSchedule
      //   && resultSchedule.schedule
      //   && resultSchedule.schedule.start_datetime
      //   && resultSchedule.schedule.end_datetime
      //   && resultSchedule.schedule.frequency
      // ) {
      //   const startDateTime = resultSchedule.schedule.start_datetime
      //     ? new Date(resultSchedule.schedule.start_datetime)
      //     : "";

      //   const endDateTime = resultSchedule.schedule.end_datetime
      //     ? new Date(resultSchedule.schedule.end_datetime)
      //     : "";

      //   const freq = resultSchedule.schedule.frequency
      //     ? {
      //       label: resultSchedule.schedule.frequency,
      //       value: resultSchedule.schedule.frequency
      //     }
      //     : "";

      //   setScheduleData(resultSchedule.schedule);
      //   setStartDate(startDateTime);
      //   setEndDate(endDateTime);
      //   setSelectedOption(freq);
      // }
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

  const onClickSaveSchedule = () => {
    setMessage("Schedule is not changeble for trial");
    // const data = {
    //   schedule: {
    //     start_datetime: startDate.toString(),
    //     end_datetime: endDate.toString(),
    //     frequency: selectedOption.value
    //   }
    // };

    // putApiary(
    //   `/projects/${props.location.state.project.name}/evaluation_schedule`,
    //   data
    // ).then(() => {
    //   setMessage(
    //     "Schedule has been saved. Inference will be executed at scheduled time"
    //   );
    //   reload();
    // });
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

  return (
    <div className="scheduling-container evaluation">
      <p className="new-dep-section font-bold">SCHEDULING</p>
      <p>{message}</p>
      <div className="container-scheduling management">
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
    </div>
  );
};

Schedule.propTypes = {
  location: PropTypes.object
};

Schedule.defaultProps = {
  location: { state: {} }
};

export default withRouter(Schedule);
