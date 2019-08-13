import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";
import EventRow from "./EventRow";
import moment from "moment";
import EntryRow from "./EntryRow";

const Timeline = props => {
  const [events, setEvents] = React.useState([]);

  React.useEffect(() => {
    BaseActions.get("events").then(result => {
      let entries = [];
      result.data.forEach(item => {
        let itemDate = moment(item.datetime)
          .format("MMMM D, YYYY")
          .toString();
        let found = entries.find(entry => entry.date === itemDate);

        if (!found) {
          let entry = {
            date: itemDate,
            data: []
          };
          entries.push(entry);
        }
      });

      result.data.forEach(item => {
        let itemDate = moment(item.datetime)
          .format("MMMM D, YYYY")
          .toString();
        entries.forEach(entry => {
          if (entry.date === itemDate) {
            entry.data.push(item);
          }
        });
      });

      entries.forEach(entry => {
        let sortedData = entry.data.sort((a, b) => {
          let dateA = new Date(a.datetime);
          let dateB = new Date(b.datetime);

          return dateB - dateA;
        });

        entry.data = sortedData;
      });

      let sortedEntries = entries.sort((a, b) => {
        let dateA = new Date(a.date);
        let dateB = new Date(b.date);

        return dateB - dateA;
      });

      setEvents(sortedEntries);
    });
  }, []);

  return (
    <Layout tab={props.tab} title="History">
      {events.length > 0 ? (
        <div
          className={
            events.length <= 1
              ? "container-timeline less-amount"
              : "container-timeline"
          }
        >
          {events.map((item, i) => {
            return <EntryRow entry={item} />;
          })}
        </div>
      ) : (
        <div className="container-timeline-empty">
          <p>It's a fresh start.</p>
          <p>There are currently no events to look at.</p>
        </div>
      )}
    </Layout>
  );
};

Timeline.propTypes = {
  tab: PropTypes.string
};

Timeline.defaultProps = {
  tab: "Timeline"
};

export default withRouter(Timeline);
