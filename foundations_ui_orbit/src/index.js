import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import * as serviceWorker from "./serviceWorker";
import "./scss/app.scss";
import App from "./js/components/App";
import SystemHealth from "./js/components/PackagePage/SystemHealth";
import NewDeployment from "./js/components/PackagePage/NewDeployment";
import ModelEvaluation from "./js/components/PackagePage/ModelEvaluation";
import Timeline from "./js/components/PackagePage/Timeline";
import ModelManagement from "./js/components/PackagePage/ModelManagement";
import Settings from "./js/components/PackagePage/Settings/Settings";
import ProjectPage from "./js/components/ProjectPage/ProjectPage";

const app = document.getElementById("root");

ReactDOM.render(
  <div className="App">
    <Router>
      <Switch>
        <Route path="/projects/:name/deployment" component={NewDeployment} />
        {/* <Route path="/performance" component={Performance} /> */}
        <Route path="/projects/:name/health" component={SystemHealth} />
        <Route path="/projects/:name/timeline" component={Timeline} />
        <Route path="/projects/:name/management" component={ModelManagement} />
        <Route path="/projects/:name/settings" component={Settings} />
        <Route path="/projects/:name/evaluation" component={ModelEvaluation} />
        <Route path="/projects" component={ProjectPage} />
        <Route path="/" component={App} />
        <Route component={App} />
      </Switch>
    </Router>
  </div>,
  app
);

serviceWorker.unregister();
