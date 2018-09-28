import React, { Component } from "react";
import ReactTable from "react-table";
import datetimeDifference from "datetime-difference";
import 'react-table/react-table.css'
import './App.css';
let columns = require('./columns');

class Queued extends Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      result: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:37722/api/v1/projects/asdf/jobs/queued")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            result: result,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, result } = this.state;
    var queuedJobs;
    queuedJobs = result.queued_jobs;

    const queued_columns = [{
      Header: 'Start Time',
      accessor: 'submitted_time'
      }, {
        Header: 'JobId',
        accessor: 'job_id'
      }, {
        Header: 'Duration in Queue',
        id: 'duration',
        accessor: 'duration'
      }, {
        Header: 'User',
        accessor: 'user'
      }
    ]

    function getTimeDifference(submitted_time){
      const currentTime = new Date();
      const dataTimeFormatted = new Date(submitted_time)
      dataTimeFormatted.setHours( dataTimeFormatted.getHours() - 4 );
      const newDate = new Date(dataTimeFormatted)
      const timeDiff = datetimeDifference(currentTime, newDate);
      return timeDiff
    }


    if (queuedJobs && queuedJobs[0]){
      queuedJobs.map(x => x.duration = getTimeDifference(x.submitted_time).days + ' days, ' + getTimeDifference(x.submitted_time).hours + ' hours, ' + getTimeDifference(x.submitted_time).minutes + ' minutes, ' + getTimeDifference(x.submitted_time).seconds + ' seconds')
    }

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <div>
            <h2>Queued Jobs</h2>
            <h3 className="project-name">Project name: {result.name}</h3>
            <h3 className="project-source">Source: not known</h3>
            <ReactTable data={queuedJobs} columns={queued_columns} />
        </div>
      );
    }
  }
}

export default Queued;