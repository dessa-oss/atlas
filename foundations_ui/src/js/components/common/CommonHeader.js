import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import ProfilePlaceholder from '../../../assets/images/icons/person-with-outline.png';

class CommonHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isProject: this.props.isProject,
    };
  }

  render() {
    const { isProject } = this.state;
    return (
      <div>
        <div className="foundations-header">
          <Link to="/projects">
            <div
              tabIndex={0}
              role="button"
              className="i--icon-dessa-logo"
            />
          </Link>

          <div className="header-link-container">
            { isProject ? <a className="font-bold" href="/projects">Project</a> : <a href="/projects">Project</a> }
            <a target="_blank" rel="noopener noreferrer" href="https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/">Documentation</a>
            <a href="/support">Support</a>
          </div>
          { process.env.REACT_APP_SCHEDULER_TYPE !== 'CE' && (
          <div className="header-container-profile">
            <img alt="" src={ProfilePlaceholder} />
            <p>CE User</p>
            <i
              onKeyPress={this.onKeyPress}
              tabIndex={0}
              role="button"
              onClick={this.onClickArrowDown}
              className="i--icon-arrow-down"
            />
          </div>
          )}
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
