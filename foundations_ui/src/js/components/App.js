import React, { Component } from 'react';
import {
  BrowserRouter as Router, Route, Switch, Redirect,
} from 'react-router-dom';
import Keycloak from 'keycloak-js';
import { KeycloakProvider } from 'react-keycloak';
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

toast.configure(); // single instance to improve rendering of toast

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { keycloak: null, authenticated: false };
  }

  componentDidMount() {
    const resp = BaseActions.getFromStaging('auth/login');
    console.log(resp);
  //   const keycloak = Keycloak('/keycloak.json');
  //   keycloak.init({ onLoad: 'login-required' }).then((authenticated) => {
  //     this.setState({ keycloak, authenticated });
  //   });
  }

  render() {
    const app = (
      <div className="App">
        <Router>
          <Switch>
            <Route exact path="/login" component={LoginPage} />
            <Route exact path="/projects" component={ProjectPage} />
            <Route exact path="/contact" component={ContactPage} />
            <Redirect exact from="/" to="/projects" />
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
    const { keycloak, authenticated } = this.state;
    if (true) {
      return true ? app : <div> not authenticated </div>;
    }
    return <Loading loadingMessage="Authenticating..." />;
  }
}

export default App;
