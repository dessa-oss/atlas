import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Select from 'react-select';
import Cookies from 'js-cookie';
import jwt from 'jwt-decode';
import LogoutActions from '../../actions/LogoutActions';
import ProfilePlaceholder from '../../../assets/images/icons/person-with-outline.png';

class CommonHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isProject: this.props.isProject,
    };
    this.onLogout = this.onLogout.bind(this);
  }

  onLogout() {
    LogoutActions.getLogout().then((response) => {
      if (response.status === 200) {
        Cookies.remove('atlas_access_token');
        Cookies.remove('atlas_refresh_token');
        this.props.history.push('/login');
      }
    });
  }

  render() {
    const { isProject } = this.state;
    const { isLoggedIn } = this.props;

    const atlasAccessToken = Cookies.get('atlas_access_token');
    let username = 'Atlas CE';

    if (atlasAccessToken) {
      const decodeToken = jwt(atlasAccessToken);
      username = decodeToken.preferred_username;
    } else {
      username = 'Atlas CE';
    }

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
          { process.env.REACT_APP_SCHEDULER_TYPE !== 'CE' && isLoggedIn && (
          <div className="header-container-profile">
            <div className="profile-container">
              <img alt="" src={ProfilePlaceholder} />
              <p>{username}</p>
            </div>
            <button onClick={this.onLogout} type="button">Log out</button>
          </div>
          )}
        </div>
      </div>
    );
  }
}

CommonHeader.propTypes = {
  isProject: PropTypes.bool,
  history: PropTypes.object,
  isLoggedIn: PropTypes.bool,
};

CommonHeader.defaultProps = {
  isProject: false,
  history: {},
  isLoggedIn: true,
};

export default CommonHeader;
