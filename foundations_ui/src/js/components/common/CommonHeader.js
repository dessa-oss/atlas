import React from 'react';
import PropTypes from 'prop-types';

class CommonHeader extends React.Component {
  render() {
    return (
      <div>
        <div className="foundations-header">
          <div className="i--icon-dessa-logo" />
          <div className="header-link-container">
            <a href="/project">Project</a>
            <a href="/documentation">Documentation</a>
            <a href="/support">Support</a>
          </div>
        </div>
      </div>
    );
  }
}

export default CommonHeader;
