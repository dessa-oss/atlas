import React, { Component } from "react";
import List from "./List";

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
    fetch("http://localhost:3000/data/")
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
    const ListItem = props  => <a href={"/" + props.text}><li className="project-items">{props.text}</li></a>;


    if (error && result[0]) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else if (result && result[0]) {
      return (
        <BrowserRouter>
          <div>
            <h3 className="project-source">Projects:</h3>
            {/* <List items={result} /> */}
            <List>
              {result.map(i => <ListItem text={i.name}/>)}
            </List>
          </div>
        </BrowserRouter>
      );
    }
  }
}

export default Home;