import React, { Component } from "react";
import ReactTable from "react-table";
import datetimeDifference from "datetime-difference";
import 'react-table/react-table.css'
import './App.css';
import rocket from './rocket.gif';
let columns = require('./columns');

class Running extends Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      result: []
    };
  }

  componentDidMount() {
    var projectName = this.props.match.params.project
    var requestURL = "http://localhost:37722/api/v1/projects/" + projectName + "/jobs/running" 
    fetch(requestURL)
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

  render(match) {
    const { error, isLoaded, result } = this.state;
    var runningJobs;
    runningJobs = result.running_jobs;

    const running_columns = [{
      Header: 'Start Time',
      accessor: 'start_time',
      minWidth: 250
    }, {
      Header: 'JobId',
      accessor: 'job_id',
      minWidth: 250
    }, {
      Header: 'Running Time',
      accessor: 'duration'
    }, {
      Header: 'User',
      accessor: 'user'
    }]

    function getTimeDifference(start_time){
      const currentTime = new Date();
      const dataTimeFormatted = new Date(start_time)
      dataTimeFormatted.setHours( dataTimeFormatted.getHours() - 4 );
      const newDate = new Date(dataTimeFormatted)
      const timeDiff = datetimeDifference(currentTime, newDate);
      return timeDiff
    }

    if (runningJobs && runningJobs[0]){
      runningJobs.map(x => x.duration = getTimeDifference(x.start_time).minutes + ' minutes, ' + getTimeDifference(x.start_time).seconds + ' seconds')
    }

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return (
        <div className="loading">
          Loading...
          <img className="rocket" src={rocket}></img>
        </div>
      )
    } else if (result.running_jobs && result.running_jobs[0]) {
      return (
        <div className="jobs">
            <h2>Running Jobs</h2>
            <h3 className="project-name">Project: {result.name}</h3>
            <ReactTable className="-highlight" data={runningJobs} columns={running_columns} />
        </div>
      );
    } else {
      const { match } = this.props;
      return (
        <div>
          <h3>No jobs running.</h3>
          <h4>Project name: {match.params.project}</h4>
        </div>
      )
    }
  }
}

export default Running