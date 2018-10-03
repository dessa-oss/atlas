import React, { Component } from "react";
import List from "./List";

import {
  Route,
  NavLink,
  BrowserRouter,
  Link,
  Switch
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
    fetch("http://localhost:37722/api/v1/projects")
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

    const List = props => <ul className="project-list">{props.children}</ul>;
    const ListItem = function(props) {
      return <li key={props.text} className="project-items">
        <h2>{props.text}</h2>
        <NavLink to={urlCreator(props.text, 'completed')}>Completed</NavLink>
        <NavLink to={urlCreator(props.text, 'queued')}>Queued</NavLink>
      </li>;

    }
    function urlCreator(name, status){
      const completedURL = `/projects/${name}/jobs/${status}`;
      return completedURL;
    }

    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) { 
      return <div>Loading...</div>;
    } else if (result && result[0]) {
      return (
        <div className="home">
          <h3 className="project-source">Projects:</h3>
            <List>
              {result.map(i => <Switch><ListItem text={i.name}/></Switch>)}
            </List>
        </div>
      );
    } else {
      return (
        <div>
          <h2>Project Listing</h2>
          <p>No project have been created––you should create one!</p>
          <p>Looking for docs, checking out the <a href="https://github.com/DeepLearnI/foundations/tree/master/examples">/examples directory</a></p>
        </div>
      );
    }
  }
}

export default Home;