import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ErrorMessage extends Component {
  constructor(props) {
    super(props);
    this.setContent = this.setContent.bind(this);
    this.setInternalServerError = this.setInternalServerError.bind(this);
    this.setNotFoundError = this.setNotFoundError.bind(this);
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
    + 'Check back again shortly.';
    return {
      errorBanner: errorBanner500,
      errorSubtext: errorSubtext500,
    };
  }

  setNotFoundError() {
    const errorBanner404 = '404 Page Not Found';
    // const errorSubtext404 = <Text>Services are having temporary issues.{'\n'}
    // Contact our front desk support at
    // <a href='mailto:support@dessa.com'>support@dessa.com</a>or{'\n'}call us toll free at 1-899-623-5578'</Text>;
    const errorSubtext404 = 'Services are having temporary issues.';
    return {
      errorBanner: errorBanner404,
      errorSubtext: errorSubtext404,
    };
  }


  render() {
    // const { notLoaded } = this.state;
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
