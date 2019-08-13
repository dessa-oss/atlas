import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";
import EventRow from "./EventRow";

const EntryRow = props => {
  return (
    <div className="container-entry">
      <div className="line" />
      <div class="circle" />
      <p className="label-entry">{props.entry.date}</p>
      <div className="timeline-entries-container">
        {props.entry.data.map((item, i) => {
          return <EventRow event={item} />;
        })}
      </div>
    </div>
  );
};

EntryRow.propTypes = {
  entry: PropTypes.object
};

EntryRow.defaultProps = {
  entry: {}
};

export default withRouter(EntryRow);
