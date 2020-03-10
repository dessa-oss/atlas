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
    this.onChangeMenu = this.onChangeMenu.bind(this);
  }

  onLogout() {
    LogoutActions.getLogout().then(response => {
      if (response.status === 200) {
        Cookies.remove('atlas_access_token');
        Cookies.remove('atlas_refresh_token');
        this.props.history.push('/login');
      }
    });
  }

  onChangeMenu(selectedOptions) {
    if (selectedOptions.value === 'logout') {
      this.onLogout();
    }
  }

  render() {
    const { isProject } = this.state;
    const { isLoggedIn } = this.props;

    const atlasAccessToken = Cookies.get('atlas_access_token');
    let username = 'Atlas';

    if (atlasAccessToken) {
      if (atlasAccessToken !== 'undefined') {
        const decodeToken = jwt(atlasAccessToken);
        username = decodeToken.preferred_username;
      }
    }

    const menuOptions = [
      {
        value: 'logout',
        label: 'Logout',
      },
    ];

    const dot = () => ({
      width: '20px',
      content: '" "',
      backgroundImage: `url(${ProfilePlaceholder})`,
      backgroundSize: '20px 20px',
      backgroundRepeat: 'no-repeat',
      visibility: 'visible',
      color: 'transparent',
      boxSizing: 'border-box',
      position: 'relative',
      top: '8px',
    });

    const menuStyles = {
      control: styles => ({
        ...styles,
        backgroundColor: '',
        color: 'white!important',
        '&:hover': {
          border: '1px solid #fff',
        },
        '&:active': {
          border: '1px solid #fff',
        },
        border: '1px solid #fff',
      }),
      dropdownIndicator: styles => ({
        ...styles,
        color: '#fff',
      }),
      option: (styles, {
        isDisabled,
        isSelected,
      }) => {
        return {
          ...styles,
          backgroundColor: '#fff',
          cursor: 'pointer',
          '&:hover': {
            backgroundColor: '#5480dc91',
          },
        };
      },
      input: styles => ({
        ...styles,
        ...dot(),
        color: 'transparent',
      }),
      placeholder: styles => ({
        ...styles,
        color: '#fff',
        marginLeft: '30px',
      }),
      singleValue: (styles, { data }) => ({ ...styles }),
    };

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
            <Select
              className="header-menu-select"
              options={menuOptions}
              placeholder={username}
              onChange={this.onChangeMenu}
              styles={menuStyles}
              components={{
                IndicatorSeparator: () => null,
              }}
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
  history: PropTypes.object,
  isLoggedIn: PropTypes.bool,
};

CommonHeader.defaultProps = {
  isProject: false,
  history: {},
  isLoggedIn: true,
};

export default CommonHeader;
