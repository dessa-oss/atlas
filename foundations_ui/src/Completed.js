import React, { Component } from "react";
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
import datetimeDifference from "datetime-difference";
import rocket from './rocket.gif';
let columns = require('./columns');

class Completed extends Component {

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
    var requestURL = "http://localhost:37722/api/v1/projects/" + projectName + "/jobs/completed" 
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
    var completedJobs;
    completedJobs = result.completed_jobs;

    const completed_columns = [{
      Header: 'Start Time',
      accessor: 'start_time',
      minWidth: 250,
    }, {
      Header: 'Status',
      accessor: 'status'
    }, {
      Header: 'JobId',
      accessor: 'job_id',
      minWidth: 250
    }, {
      Header: 'Duration',
      id: 'duration',
      accessor: 'duration'
    }, {
      Header: 'User',
      accessor: 'user'
    }]

    if (result.completed_jobs && result.completed_jobs[0]) {

      // completed_jobs is a list of job objects
      var finalResult = result.completed_jobs.map(function(x){
        var obj = x.input_params;
      
        // group by name value into list to create unique name
        var groupBy = obj.reduce((acc, curr) => {
            if(!acc[curr.name]) acc[curr.name] = [];
            acc[curr.name].push(curr);
            return acc;
          },{});
        
        // loop through all grouped lists and update name
        // return update input params dict
        Object.keys(groupBy).map(function(key) {
              if (groupBy[key].length > 1){
                  groupBy[key].map(function(x, index){
                      x.name = x.name + '_' + (index + 1)
                  })
              }
          });

        var finalInputDict = {};
        for (var key in groupBy){
          groupBy[key].map(function(y) {
            finalInputDict[y.name] = y;
          })
        }

        x.input_params_dict = finalInputDict;
        return x;
      })

      // finalResult is list of objects
      // each with input_params_dict which is unique key dict
      var input_params_dict = finalResult[0].input_params_dict
      var keys = Object.keys(input_params_dict)

      // loop over all input_params_dict and create union
      var allParams = []
      Object.keys(finalResult).map(function(key){
        finalResult[key].input_params.map(function(param){
          allParams.push(param.name)
        })
      })

      // unique list of all strings input params
      var uniqueParams = [...new Set(allParams)];

      // Create columns
      uniqueParams.map(function(key){
        var columnName = key;
        var obj = {};
        obj['Header'] = 'Input: ' + columnName;
        obj['accessor'] = job => determineValue(key, job);
        obj['id'] = Math.random(10).toString();
        obj['minWidth'] = 200
        completed_columns.push(obj);
      })

      Object.keys(finalResult[0].output_metrics).map(function(key){
        var columnName = key;
        var obj = {};
        obj['Header'] = 'Output: ' + columnName;
        obj['accessor'] = job => JSON.stringify(job.output_metrics[key]);
        obj['id'] = Math.random(10).toString();
        obj['minWidth'] = 200
        completed_columns.push(obj);
      })

      function getTimeDifference(start, complete){
        const initial_time = new Date(start);
        const complete_time = new Date(complete);
        const timeDiff = datetimeDifference(initial_time, complete_time);
        return timeDiff;
      }

      completedJobs.map(x => x.duration = getTimeDifference(x.start_time, x.completed_time).minutes + 'm:' + getTimeDifference(x.start_time, x.completed_time).seconds + 's')
      
      // Convert time to local timezone
      function updateTime(timeString){
        var timeStamp = new Date(timeString);
        timeStamp.setHours( timeStamp.getHours() - 4 );
        var ISODateFormat = new Date(timeStamp).toLocaleString('en-GB');
        var yearFormat = ISODateFormat.split(',')[0].split('/').reverse().join('/')
        var finalISO = yearFormat + ISODateFormat.split(',')[1]
        return finalISO;
      }

      completedJobs.map(x => x.start_time = updateTime(x.start_time))

      function determineValue(index, job){
        if (job.input_params_dict[index]) {
          var obj = job.input_params_dict[index].value
          if (obj.type === 'stage'){
            return obj.stage_name;
          } else if (obj.type === 'constant'){
            return obj.value;
          } else if (obj.type === 'dynamic') {
            var jobParams = job.job_parameters;
            return jobParams[obj.name];
          }
        }
      }
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
    } else if (result.completed_jobs && result.completed_jobs[0]) {
      return (
        <div className="jobs">
            <h2>Completed Jobs</h2>
            <h3 className="project-name">Project: {result.name}</h3>
            <ReactTable className="-highlight" data={completedJobs} columns={completed_columns} defaultSorted={[{id: "start_time",desc: true}]} />
        </div>
      );
    } else {
      const { match } = this.props;
      return (
        <div>
          <h3>No jobs completed yet.</h3>
          <h4>Project name: {match.params.project}</h4>
        </div>
      )
    }
  }
}

export default Completed