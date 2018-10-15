import React, { Component } from "react";
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
import rocket from './rocket.gif';
import { updateTime, createTimeStamp } from './utils';

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
    var projectName = this.props.match.params.project
    var requestURL = "http://localhost:37722/api/v1/projects/" + projectName + "/jobs/queued"
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

  render() {
    const { error, isLoaded, result } = this.state;
    var queuedJobs;
    queuedJobs = result.queued_jobs;

    const queued_columns = [{
        Header: 'Submitted',
        accessor: 'submitted_time'
      }, {
        Header: 'JobId',
        accessor: 'job_id'
      }, {
        Header: 'Queued Time',
        id: 'duration',
        accessor: 'duration'
      }, {
        Header: 'User',
        accessor: 'user'
      }
    ]

    if (queuedJobs && queuedJobs[0]){
      queuedJobs.map(job => job.submitted_time = updateTime(job.submitted_time))
      createTimeStamp(queuedJobs, 'submitted_time')
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
    } else {
      return (
        <div className="jobs">
            <h2>Queued Jobs</h2>
            <h3 className="project-name">Project name: {result.name}</h3>
            <ReactTable data={queuedJobs} columns={queued_columns} defaultSorted={[{id: "submitted_time",desc: true}]} />
        </div>
      );
    }
  }
}

export default Queued;
