import React, { Component } from "react";
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
import rocket from './rocket.gif';
import { updateTime, getTimeDifference, createTimeStamp } from './utils';

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
      accessor: 'start_time'
    }, {
      Header: 'JobId',
      accessor: 'job_id'
    }, {
      Header: 'Running Time',
      accessor: 'duration'
    }, {
      Header: 'User',
      accessor: 'user'
    }]

    if (runningJobs && runningJobs[0]){
      runningJobs.map(job => job.start_time = updateTime(job.start_time))
      createTimeStamp(runningJobs, 'start_time')
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
            <ReactTable className="-highlight" data={runningJobs} columns={running_columns} defaultSorted={[{id:"start_time",desc: true}]} />
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
