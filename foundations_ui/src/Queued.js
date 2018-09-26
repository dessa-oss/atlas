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
    fetch("http://localhost:3000/data")
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
      accessor: 'findDiff(submitted_time)'
    }, {
      Header: 'User',
      accessor: 'user'
    }
  ]

  function findDiff(dataTime) {
    const date1 = new Date("2017-09-21 14:19:54");
    const date2 = new Date("2/21/2018, 07:12:42 AM");
    const diff = datetimeDifference(date1, date2);
    return diff;
  }


    // const date1 = new Date("2017-09-21 14:19:54");
    // const date2 = new Date("2/21/2018, 07:12:42 AM");
    // const diff = datetimeDifference(date1, date2);
    // console.log(diff)

    if (queuedJobs && queuedJobs[0]){
      // console.log('time from server: ', queuedJobs[0].submitted_time)
      // console.log('time for diff: ', "2/21/2017, 07:12:42 AM")
      // var currentTime = new Date();
      // console.log(currentTime)
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