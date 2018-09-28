import React, { Component } from 'react';
import Home from "./Home";
import Queued from "./Queued";
import Completed from "./Completed";
import logo from './dessa_logo.svg';
import './App.css';
import {
  Route,
  NavLink,
  BrowserRouter
  } from "react-router-dom";

class App extends Component {

  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Foundations</h1>
            <ul className="header">
              <li><NavLink exact to="/">Home</NavLink> </li>
              <li><NavLink to="/completed">Completed</NavLink></li>
              <li><NavLink to="/queued">Queued</NavLink></li>
            </ul>
          </header>
          <div className="content">
            <Route exact path="/" component={Home} />
            <Route path="/queued" component={Queued} />
            <Route path="/completed" component={Completed} />
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
