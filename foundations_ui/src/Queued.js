import React, { Component } from "react";
import ReactTable from "react-table";
import datetimeDifference from "datetime-difference";
import 'react-table/react-table.css'
import './App.css';
import rocket from './rocket.gif';

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
        Header: 'Duration',
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
      queuedJobs.map(x => x.duration = getTimeDifference(x.submitted_time).minutes + 'm:' + getTimeDifference(x.submitted_time).seconds + 's')

      // Convert time to local timezone
      function updateTime(timeString){
        var timeStamp = new Date(timeString);
        timeStamp.setHours( timeStamp.getHours() - 4 );
        var ISODateFormat = new Date(timeStamp).toLocaleString('en-GB');
        var yearFormat = ISODateFormat.split(',')[0].split('/').reverse().join('/')
        var finalISO = yearFormat + ISODateFormat.split(',')[1]
        return finalISO;
      }

      queuedJobs.map(x => x.submitted_time = updateTime(x.submitted_time))
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