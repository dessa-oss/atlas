import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import './scss/app.scss';
import App from './js/components/App';

const app = document.getElementById('root');

ReactDOM.render(
  <App />,
  app,
);

serviceWorker.unregister();
