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
    fetch("http://localhost:3000/")
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
    var completedJobs;
    completedJobs = result;

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {  
      return (
        <div>
            <h2>Completed Jobs</h2>
            <h3 className="project-name">Project name: {result.name}</h3>
            <h3 className="project-source">Source: not known</h3>
            <ReactTable data={completedJobs} columns={columns.completed_columns} />
        </div>
      );
    }
  }
}

export default Completed;