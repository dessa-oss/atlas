import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";
import moment from "moment";

const EventRow = props => {
  // TO MODIFY WHEN JSON HAS TYPE
  let labelClassName = "label-event-type type-inference";
  let labelText = "INFERENCE";
  let labelStatusClassname = "label-event-status event-status-success";

  if (props.event.event_category === "input data") {
    labelClassName = "label-event-type type-input";
    labelText = "INPUT DATA";
  }

  if (props.event.event_category === "feedback data") {
    labelClassName = "label-event-type type-feedback";
    labelText = "INPUT FEEDBACK";
  }

  if (props.event.event_category === "project") {
    labelClassName = "label-event-type type-project";
    labelText = "PROJECT";
  }

  if (props.event.event_category === "deployment") {
    labelClassName = "label-event-type type-deployment";
    labelText = "DEPLOYMENT";
  }

  if (props.event.event_category === "recalibration") {
    labelClassName = "label-event-type type-recalibration";
    labelText = "RECALIBRATION";
  }

  if (props.event.type === "error") {
    labelStatusClassname = "label-event-status event-status-error";
  }

  if (props.event.type === "warning") {
    labelStatusClassname = "label-event-status event-status-warning";
  }

  return (
    <div className="container-event">
      <div className="label-event-time">
        {moment(props.event.datetime)
          .format("hh:mm a")
          .toString()}
      </div>
      <div className="container-event-info">
        <div className="container-event-type">
          <div className={labelClassName}>{labelText}</div>
        </div>
        <div className={labelStatusClassname}>
          {props.event.type}
          <div className="status-circle" />
        </div>
        <div className="label-event-message">{props.event.message}</div>
      </div>
    </div>
  );
};

EventRow.propTypes = {
  event: PropTypes.object
};

EventRow.defaultProps = {
  event: {}
};

export default withRouter(EventRow);
