import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ErrorMessage extends Component {
  constructor(props) {
    super(props);
    this.setContent = this.setContent.bind(this);
    this.setInternalServerError = this.setInternalServerError.bind(this);
    this.setNotFoundError = this.setNotFoundError.bind(this);
    this.setBadRequestError = this.setBadRequestError.bind(this);
    this.state = {
      errorCode: this.props.errorCode,
    };
  }

  setContent() {
    const { errorCode } = this.state;
    if (errorCode === 404) {
      return this.setNotFoundError();
    }
    if (errorCode === 500) {
      return this.setInternalServerError();
    }
    if (errorCode === 400) {
      return this.setBadRequestError();
    }
    console.log('Error code not valid');

    return {
      errorBanner: '',
      errorSubtext: '',
    };
  }

  setInternalServerError() {
    const errorBanner500 = '500 Internal Server Error';
    const errorSubtext500 = 'Our servers are having problems '
    + 'going through the astroid belts.'
    + ' Check back again shortly.';
    return {
      errorBanner: errorBanner500,
      errorSubtext: errorSubtext500,
    };
  }

  setNotFoundError() {
    const errorBanner404 = '404 Page Not Found';
    const errorSubtext404 = 'Services are having temporary issues.'
    + ' Contact our front desk support at support@dessa.com or call us toll free at 1-899-623-5578.';
    return {
      errorBanner: errorBanner404,
      errorSubtext: errorSubtext404,
    };
  }

  setBadRequestError() {
    const errorBanner400 = '400 Bad Request Error';
    const errorSubtext400 = 'The request was malformed, please try a proper request.';
    return {
      errorBanner: errorBanner400,
      errorSubtext: errorSubtext400,
    };
  }


  render() {
    const { errorBanner, errorSubtext } = this.setContent();

    return (
      <div className="error-body-container">
        <div className="i--icon-astronaut-probs text-center" />
        <h1 className="blue-border-bottom font-bold">Houston, we have a problem.</h1>
        <h2 className="font-bold">{errorBanner}</h2>
        <p>{errorSubtext}</p>
      </div>
    );
  }
}

ErrorMessage.propTypes = {
  errorCode: PropTypes.number,
};

ErrorMessage.defaultProps = {
  errorCode: 404,
};

export default ErrorMessage;
