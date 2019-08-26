import React from 'react';
import PropTypes from 'prop-types';
import ProfilePlaceholder from '../../../assets/images/icons/profile-placeholder.png';

class CommonHeader extends React.Component {
  onKeyPress() {}

  onClickArrowDown() {}

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
          <div className="header-container-profile">
            <img alt="" src={ProfilePlaceholder} />
            <p>Mohammed R.</p>
            <i
              onKeyPress={this.onKeyPress}
              tabIndex={0}
              role="button"
              onClick={this.onClickArrowDown}
              className="i--icon-arrow-down"
            />
          </div>
        </div>
      </div>
    );
  }
}

export default CommonHeader;
