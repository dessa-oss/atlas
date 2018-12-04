import React from 'react';
import ReactDOM from 'react-dom';
import App from '../js/components/App';

it('Renders App', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});
