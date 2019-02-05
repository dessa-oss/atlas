import React, { Component } from 'react';
import PropTypes from 'prop-types';

class LoginHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pageTitle: this.props.pageTitle,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ pageTitle: nextProps.pageTitle });
  }

  render() {
    const { pageTitle } = this.state;

    return (
      <div className="project-header-container">
        <div className="project-header-logo-container">
          <div className="i--icon-logo" />
          <h2 className="font-bold">Foundations</h2>
        </div>
        <div className="project-header-info-container">
          <div className="project-header-total-projects-container">
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">{ pageTitle }</h1>
            </div>
          </div>
          <div className="project-header-sort-filter-container" />
        </div>
      </div>
    );
  }
}

LoginHeader.propTypes = {
  pageTitle: PropTypes.string,
};

LoginHeader.defaultProps = {
  pageTitle: '',
};

export default LoginHeader;
