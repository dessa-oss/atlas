import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import Cookies from 'js-cookie';
import Toolbar from '../common/Toolbar';
import LoginActions from '../../actions/LoginActions';
import Header from '../common/Header';
import ErrorMessage from '../common/ErrorMessage';
import CommonHeader from '../common/CommonHeader';


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
    this.login = this.login.bind(this);
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
    this.login(username, password);
    event.preventDefault();
  }

  async login(username, password) {
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
      passwordError = 'Incorrect password';
    }

    if (loginResponse.status === 400) {
      return <ErrorMessage errorCode={loginResponse[0]} />;
    }

    return (
      <div className="login-page-container">
        <CommonHeader {...this.props} />
        <div className="login-body-container">
          <h3>Welcome back!</h3>
          <form onSubmit={this.handleSubmit}>
            <ul>
              <li>
                <input
                  className="login-form-username"
                  type="username"
                  name="username"
                  value={username}
                  onChange={this.handleUsernameChange}
                  placeholder="username"
                />
              </li>
              <li>
                <input
                  className="login-form-password"
                  type="password"
                  name="password"
                  value={password}
                  onChange={this.handlePasswordChange}
                  placeholder="password"
                />
              </li>
              <li>
                <input className="login-submit" type="submit" value="Login" />
              </li>
              <li>
                <p className="auth-error">{passwordError}</p>
              </li>
            </ul>
          </form>
          <h4>Don&#39;t have an account? <a href="/support">Get Started</a></h4>
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
