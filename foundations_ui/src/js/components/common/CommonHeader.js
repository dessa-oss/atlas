import React from 'react';
import PropTypes from 'prop-types';
import ProfilePlaceholder from '../../../assets/images/icons/profile-placeholder.png';

class CommonHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isProject: this.props.isProject,
    };
  }

  onKeyPress() {}

  onClickArrowDown() {}

  render() {
    const { isProject } = this.state;
    return (
      <div>
        <div className="foundations-header">
          <div className="i--icon-dessa-logo" />
          <div className="header-link-container">
            { isProject ? <a className="font-bold" href="/projects">Project</a> : <a href="/projects">Project</a> }
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

CommonHeader.propTypes = {
  isProject: PropTypes.bool,
};

CommonHeader.defaultProps = {
  isProject: false,
};

export default CommonHeader;
