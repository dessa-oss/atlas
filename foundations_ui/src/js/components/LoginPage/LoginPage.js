import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import Cookies from 'js-cookie';
import Toolbar from '../common/Toolbar';
import LoginActions from '../../actions/LoginActions';
import Header from '../common/Header';
import ErrorMessage from '../common/ErrorMessage';

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: null,
      loginResponse: [],
      username: '',
      password: '',
    };
    this.handleUsernameChange = this.handleUsernameChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleUsernameChange(event) {
    this.setState({
      username: event.target.value,
    });
    event.preventDefault();
  }

  handlePasswordChange(event) {
    this.setState({
      password: event.target.value,
    });
    event.preventDefault();
  }

  handleSubmit(event) {
    const { username, password, loginResponse } = this.state;
    LoginActions.getLogin(username, password).then((res) => {
      if (res.status === 200) {
        this.setState({
          loginResponse: res,
          isLoggedIn: true,
        });
      } else {
        this.setState({
          loginResponse: res,
          isLoggedIn: false,
        });
      }
    });
    event.preventDefault();
  }

  render() {
    const {
      isLoggedIn,
      loginResponse,
      username,
      password,
    } = this.state;

    let passwordError;

    if (isLoggedIn) {
      this.props.history.push('/projects');
    }

    if (loginResponse.status === 401) {
      passwordError = 'Incorrect password.';
    }

    if (loginResponse.status === 400) {
      return <ErrorMessage errorCode={loginResponse[0]} />;
    }

    return (
      <div className="login-page-container">
        <div className="header">
          <Header pageTitle="Login" />
        </div>
        <div className="login-body-container">
          <form onSubmit={this.handleSubmit}>
            <ul>
              <li>
                <label>
                  Username:
                  <input type="username" name="username" value={username} onChange={this.handleUsernameChange} />
                </label>
              </li>
              <li>
                <label>
                  Password:
                  <input type="password" name="password" value={password} onChange={this.handlePasswordChange} />
                </label>
              </li>
              <input type="submit" value="Submit" />
            </ul>
          </form>
          <p className="auth-error">{passwordError}</p>
        </div>
      </div>
    );
  }
}

LoginPage.propTypes = {
  isMount: PropTypes.bool,
  isLoggedIn: PropTypes.bool,
  isLoaded: PropTypes.bool,
  loginResponse: PropTypes.array,
  history: PropTypes.object,
};

LoginPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  isLoggedIn: false,
  loginResponse: [],
  history: {},
};

export default LoginPage;
