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

  render(match) {
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
            <Route path="/projects/:project/jobs/queued" component={Queued}/>
            {/* <Route path="/projects/:project/jobs/completed" component={Completed}/> */}
            <Route
              path="/projects/:project/jobs/completed"
              render={props => {
                const {
                  match: {
                    params: { project }
                  }
                } = props;
                return (
                  <Completed
                    key={`project=${project}`}
                    {...props}
                  />
                );
              }}
            />
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
