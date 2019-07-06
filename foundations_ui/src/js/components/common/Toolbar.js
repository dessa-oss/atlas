import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Toolbar extends Component {
  render() {
    return (
      <div className="toolbar-container">
        <div className="job-header-logo-container">
          <Link to="/projects">
            <div className="i--icon-logo" />
          </Link>
          <h2 className="font-bold">Foundations</h2>
        </div>
        <ul className="header-links">
          <li>
            <Link to="/projects">Projects</Link>
          </li>
          <li>
            <Link to="/documentation">Documentation</Link>
          </li>
          <li>
            <Link to="/support">Contact Support</Link>
          </li>
        </ul>
      </div>
    );
  }
}

export default Toolbar;
