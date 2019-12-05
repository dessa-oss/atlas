import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import EventRow from "./EventRow";

const EntryRow = props => {
  const { entry } = props;

  return (
    <div className="container-entry">
      <div className="line" />
      <div className="circle" />
      <p className="label-entry">{entry.date}</p>
      <div className="timeline-entries-container">
        {entry.data.map(item => {
          return <EventRow key={item.datetime} event={item} />;
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
