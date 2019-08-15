import React from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { get } from "../../../actions/BaseActions";
import moment from "moment";
import EntryRow from "./EntryRow";

const Timeline = props => {
  const [events, setEvents] = React.useState([]);

  React.useEffect(() => {
    get("events").then(result => {
      if (result) {
        const entries = [];
        result.data.forEach(item => {
          const itemDate = moment(item.datetime)
            .format("MMMM D, YYYY")
            .toString();
          const found = entries.find(entry => entry.date === itemDate);

          if (!found) {
            const entry = {
              date: itemDate,
              data: []
            };
            entries.push(entry);
          }
        });

        result.data.forEach(item => {
          const itemDate = moment(item.datetime)
            .format("MMMM D, YYYY")
            .toString();
          entries.forEach(entry => {
            if (entry.date === itemDate) {
              entry.data.push(item);
            }
          });
        });

        const newEntries = entries.map(entry => {
          const newEntry = entry;
          const sortedData = entry.data.sort((a, b) => {
            const dateA = new Date(a.datetime);
            const dateB = new Date(b.datetime);

            return dateB - dateA;
          });

          newEntry.data = sortedData;
          return newEntry;
        });

        const sortedEntries = newEntries.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);

          return dateB - dateA;
        });

        setEvents(sortedEntries);
      }
    });
  }, []);

  const { tab } = props;

  return (
    <Layout tab={tab} title="History">
      {events.length > 0 ? (
        <div
          className={
            events.length <= 1
              ? "container-timeline less-amount"
              : "container-timeline"
          }
        >
          {events.map(item => {
            return <EntryRow key={item.date} entry={item} />;
          })}
        </div>
      ) : (
        <div className="container-timeline-empty">
          <p>It{"'"}s a fresh start.</p>
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
