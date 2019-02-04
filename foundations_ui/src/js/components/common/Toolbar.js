import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Toolbar extends Component {
  render() {
    return (
      <div className="toolbar-container">
        <Link to="/projects">Home</Link>
        <p>Support and Contact</p>
      </div>
    );
  }
}

export default Toolbar;
