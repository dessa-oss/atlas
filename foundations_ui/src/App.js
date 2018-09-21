import React, { Component } from 'react';
import ReactTable from "react-table";

import logo from './dessa_logo.svg';
import 'react-table/react-table.css'
import './App.css';
let columns = require('./columns');

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      result: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:3000/completed_jobs")
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
    var data;
    data = result;

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Foundations</h1>
            <h1 className="App-docs">Docs</h1>
          </header>
          <div className="App-body">
            <h1 className="project-name">Project name: Detect Supernovas</h1>
            <h3 className="project-source">Source: /tmp/foundations/test-foundations</h3>
            <ReactTable
              data={data}
              columns={columns.columns}
            />
          </div>
        </div>
      );
    }
  }
}

export default App;
