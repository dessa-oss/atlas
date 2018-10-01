import React, { Component } from "react";
<<<<<<< HEAD
// import List from "./List";
=======
import List from "./List";
>>>>>>> f0d5a868057bd6b770c0d0a47408cdf2a5ec6f1e
import {
  Route,
  NavLink,
  BrowserRouter
  } from "react-router-dom";
import 'react-table/react-table.css'
import './App.css';
import ReactTable from "react-table";
let columns = require('./columns');

class Home extends Component {

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
    var projects;
    projects = result;

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <BrowserRouter>
          <div>
            <h2>Completed Jobs</h2>
            <h1 className="project-name">Project name: </h1>
            <h3 className="project-source">Source: not known</h3>
            <List items={result} />
          </div>
        </BrowserRouter>
      );
    }
  }
}

export default Home;