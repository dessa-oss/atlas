import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import LoginActions from '../../actions/LoginActions';
import LoginHeader from './LoginHeader';

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loginStatus: null,
      value: '',
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    const data = new FormData(event.target);
    fetch('http://127.0.0.1:37722/api/v1/login', {
      method: 'post',
      body: data,
    });
    event.preventDefault();
  }

  async login() {
    const loginStatus = await LoginActions.getProjects();
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      this.setState({ loginStatus: loginStatus});
    }
  }

  render() {
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
              <input type="text" name="password" value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
          </form>

        </div>
      </div>
    );
  }
}

LoginPage.propTypes = {
  isMount: PropTypes.bool,
  loginStatus: PropTypes.bool,
};

LoginPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  queryStatus: 200,
  loginStatus: false,
};

export default LoginPage;
