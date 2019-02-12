import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import LoginActions from '../../actions/LoginActions';
import LoginHeader from './LoginHeader';
import ErrorMessage from '../common/ErrorMessage';

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: null,
      loginResponse: [],
      value: '',
    };
    this.login = this.login.bind(this);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    const data = new FormData(event.target);
    this.login(data);
    event.preventDefault();
  }

  async login(data) {
    const response = await LoginActions.postLogin(data);
    this.setState({
      loginResponse: response,
      isLoggedIn: response[0] === 200,
    });
  }

  render() {
    const { isLoggedIn, loginResponse } = this.state;

    let passwordError;
    if (isLoggedIn) {
      return LoginActions.redirect('/projects');
    }

    if (loginResponse[0] === 401) {
      passwordError = 'Incorrect password.';
    }

    if (loginResponse[0] === 400) {
      return <ErrorMessage errorCode={loginResponse[0]} />;
    }

    return (
      <div className="login-page-container">
        <div className="header">
          <Toolbar />
          <LoginHeader pageTitle="Login" />
        </div>
        <div className="login-body-container">
          <form onSubmit={this.handleSubmit}>
            <label>
              Password:
              <input type="password" name="password" value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
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
};

LoginPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  isLoggedIn: false,
  loginResponse: [],
};

export default LoginPage;
