import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

// dependencies
// import { Provider } from "react-redux";


// import { userIsAuthenticatedRedir } from './js/auth/auth';
// can also use userIsNotAuthenticatedRedir

// Entrypoint for css. (using sass)
import './scss/app.scss';

// Page components.  Should we move this to a pages folder?
// import Login from "./js/components/login/Login";
// import Register from "./js/components/register/Register";
// import Landing from "./js/components/landing/Landing";
import App from './js/components/App';

// The Redux store file
// import store from "./js/store";

// React app insertion
const app = document.getElementById('root');

// react router - client side routing
// Removed below initial routing until login/authentication exists
// <Route path="/login"  component={Login}></Route>
// <Route path="/register"  component={Register} ></Route>
// <Route path="/landing"  component={userIsAuthenticatedRedir(Landing)}></Route>
// <Route path="/" component={Login} />
// <Route component={Login} />
// ReactDOM.render(<Provider store={store}>
ReactDOM.render(
  <Router>
    <div>
      <Switch>
        <Route path="/" component={App} />
        <Route component={App} />
      </Switch>
    </div>
  </Router>, app,
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
