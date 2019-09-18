import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ErrorPage extends Component {
  constructor(props) {
    super(props);

    this.onClickBack = this.onClickBack.bind(this);
  }

  onClickBack() {
    const { history } = this.props;
    history.push('/');
  }

  render() {
    return (
      <div className="page-error-container">
        <h1 className="font-bold">Well, this is awkward.</h1>
        <h1 className="font-bold">404</h1>
        <h2 className="font-bold">The page you requested was not found.</h2>
        <h2
          className="font-bold underline"
          onClick={this.onClickBack}
          onKeyDown={() => {}}
        >
          Go back to the Projects page.
        </h2>
        <div className="error-page-image" />
      </div>
    );
  }
}

ErrorPage.propTypes = {
  history: PropTypes.object,
};

ErrorPage.defaultProps = {
  history: {},
};

export default ErrorPage;
