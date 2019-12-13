import React, { Component } from 'react';
import {
  BrowserRouter as Router, Route, Switch, Redirect,
} from 'react-router-dom';
import { toast } from 'react-toastify';
import ProjectPage from './ProjectPage/ProjectPage';
import LoginPage from './LoginPage/LoginPage';
import ContactPage from './ContactPage/ContactPage';
import ErrorMessage from './common/ErrorMessage';
import 'react-toastify/dist/ReactToastify.css';
import ProjectOverview from './JobOverviewPage/ProjectOverview';
import JobDetails from './JobOverviewPage/JobDetails';
import SupportPage from './SupportPage/SupportPage';
import Loading from './common/Loading';
import BaseActions from '../actions/BaseActions';
import LoginActions from '../actions/LoginActions';

toast.configure(); // single instance to improve rendering of toast

class App extends Component {
  render() {
    const app = (
      <div className="App">
        <Router>
          <Switch>
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/projects" component={ProjectPage} />
            <Route exact path="/contact" component={ContactPage} />
            <Redirect exact from="/" to="/login" />
            <Route
              path="/projects/:projectName/job_listing"
              component={JobDetails}
            />
            <Route
              path="/projects/:projectName/overview"
              component={ProjectOverview}
            />
            <Route exact path="/support" component={SupportPage} />
            <Route render={() => <ErrorMessage errorCode={404} />} />
          </Switch>
        </Router>
      </div>
    );
    return app;
  }
}

export default App;
