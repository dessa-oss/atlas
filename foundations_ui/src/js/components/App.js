import React, { Component } from 'react';
import {
  BrowserRouter as Router, Route, Switch, Redirect,
} from 'react-router-dom';
import PropTypes from 'prop-types';
import ProjectPage from './ProjectPage/ProjectPage';
import JobListPage from './JobListPage/JobListPage';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route exact path="/projects" component={ProjectPage} />
            <Redirect exact from="/" to="/projects" />
            <Route
              path="/projects/job_listing/:projectName/"
              component={JobListPage}
            />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
