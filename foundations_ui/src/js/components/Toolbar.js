import React, { Component } from 'react';

class Toolbar extends Component {
  render() {
    return (
      <div className="toolbar-container">
        <div className="toolbar-home">
          <p className="toolbar-item toolbar-home-text">Home</p>
        </div>
        <div className="toolbar-support">
          <p className="toolbar-item toolbar-support-text">Support and Contact</p>
        </div>
      </div>
    );
  }
}

export default Toolbar;
