import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import ProjectActions from '../../actions/ProjectActions';
import LoginHeader from './LoginHeader';

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    alert(`A name was submitted: ${this.state.value}`);
    event.preventDefault();
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
              <input type="text" value={this.state.value} onChange={this.handleChange} />
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
  isLoaded: PropTypes.bool,
  queryStatus: PropTypes.number,
  projects: PropTypes.array,
};

LoginPage.defaultProps = {
  isMount: false,
  isLoaded: false,
  queryStatus: 200,
  projects: [],
};

export default LoginPage;
