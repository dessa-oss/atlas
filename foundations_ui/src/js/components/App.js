import React, { Component } from 'react';
import {
  BrowserRouter as Router, Route, Switch, Redirect,
} from 'react-router-dom';
import PropTypes from 'prop-types';
import ProjectPage from './ProjectPage/ProjectPage';
import LoginPage from './LoginPage/LoginPage';
import JobListPage from './JobListPage/JobListPage';
import ErrorMessage from './common/ErrorMessage';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/projects" component={ProjectPage} />
            <Redirect exact from="/" to="/projects" />
            <Route
              path="/projects/:projectName/job_listing"
              component={JobListPage}
            />
            <Route render={() => <ErrorMessage errorCode={404} />} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
