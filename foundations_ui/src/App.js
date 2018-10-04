import React, { Component } from 'react';
import Home from "./Home";
import Queued from "./Queued";
import Completed from "./Completed";
import Running from "./Running";
import logo from './dessa_logo.svg';
import './App.css';
import {
  Route,
  NavLink,
  BrowserRouter
  } from "react-router-dom";

class App extends Component {

  render(match) {
    return (
      <BrowserRouter>
        <div className="App">
          <header className="App-header">
          <NavLink exact to="/"><img src={logo} className="App-logo" alt="logo" /></NavLink>
            <h1 className="App-title"><NavLink exact to="/">Foundations</NavLink></h1>
            <ul className="header">
              <li><NavLink exact to="/">Home</NavLink></li>
            </ul>
          </header>
          <div className="content">
            <Route exact path="/" component={Home} />
            <Route path="/projects/:project/jobs/queued" component={Queued}/>
            <Route path="/projects/:project/jobs/completed" component={Completed}/>
            <Route path="/projects/:project/jobs/running" component={Running}/>
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
