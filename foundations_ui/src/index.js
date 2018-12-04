import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';
import './scss/app.scss';
import App from './js/components/App';

const app = document.getElementById('root');

ReactDOM.render(
  <Router>
    <Switch>
      <Route path="/" component={App} />
      <Route component={App} />
    </Switch>
  </Router>, app,
);

serviceWorker.unregister();
