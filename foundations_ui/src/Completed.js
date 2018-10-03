import React, { Component } from "react";
import ReactTable from "react-table";
import 'react-table/react-table.css'
import './App.css';
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
      minWidth: 250
    }, {
      Header: 'Status',
      accessor: 'status'
    }, {
      Header: 'JobId',
      accessor: 'job_id',
      minWidth: 250
    }, {
      Header: 'User',
      accessor: 'user'
    }
  ]



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
        // return update input params list
        Object.keys(groupBy).map(function(key) {
              if (groupBy[key].length > 1){
                  groupBy[key].map(function(x, index){
                      x.name = x.name + '_' + (index + 1)
                  })
              }
          });
          
        var finalInputList = [];
        for (var key in groupBy){
          groupBy[key].map(y => finalInputList.push(y))
        }

        x.input_params = finalInputList;
        return x;        
      })
      
      finalResult[0].input_params.map(function(input_param, index){
        var columnName = input_param.name;
        var obj = {};
        obj['Header'] = 'Input: ' + columnName;
        obj['accessor'] = job => determineValue(index, job);
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
        completed_columns.push(obj);
      })
      

      function determineValue(index, job){
        var obj = job.input_params[index].value
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

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else if (result.completed_jobs && result.completed_jobs[0]) {
      return (
        <div>
            <h2>Completed Jobs</h2>
            <h3 className="project-name">Project: {result.name}</h3>
            <h3 className="project-source">Source: not known</h3>
            <ReactTable data={completedJobs} columns={completed_columns} />
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