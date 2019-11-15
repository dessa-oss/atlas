/* eslint-disable max-len */
/* eslint-disable no-trailing-spaces */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';
import CommonHeader from '../common/CommonHeader';
import CommonFooter from '../common/CommonFooter';

class SupportPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoggedIn: Cookies.get('atlas_refresh_token') !== undefined,
    };

    this.onClickStackOverflow = this.onClickStackOverflow.bind(this);
    this.onClickEmailUs = this.onClickEmailUs.bind(this);
    this.onClickSales = this.onClickSales.bind(this);
  }

  onClickStackOverflow() {
    window.location = 'https://stackoverflow.com/questions/ask';
  }

  onClickEmailUs() {
    window.location = 'mailto:foundations@dessa.com';
  }

  onClickSales() {
    window.location = 'mailto:deploy@dessa.com?subject=Foundations Enterprise';
  }

  render() {
    const { isLoggedIn } = this.state;
    return (
      <div>
        <CommonHeader {...this.props} isLoggedIn={isLoggedIn} />
        <div className="support-page-container">
          <div>
            <h2 className="font-bold">Got a technical question?</h2>
            <p>We are active on StackOverflow and monitoring the foundations-atlas tag. Help build the community by asking the question publicly.
            </p>
            <div tabIndex={0} role="button" onKeyPress={this.onClickStackOverflow} onClick={this.onClickStackOverflow}>
              <h2 className="font-bold">Ask on StackOverflow</h2>
            </div>
          </div>
          <div>
            <h2 className="font-bold">Need immediate help?</h2>
            <p>If the documentation and StackOverflow weren&apos;t helpful you can reach out to us via e-mail.
            </p>
            <div
              tabIndex={0}
              role="button"
              onKeyPress={this.onClickEmailUs}
              onClick={this.onClickEmailUs}
            >
              <h2 className="font-bold">E-mail Us</h2>
            </div>
          </div>
          <div>
            <h2 className="font-bold">Get Foundations Enterprise</h2>
            <p>Love using Foundations? Want to implement it for your team? Or want to learn more about what Enterprise
              version has to offer? Get in touch with us.
            </p>
            <div
              tabIndex={0}
              role="button"
              onKeyPress={this.onClickSales}
              onClick={this.onClickSales}
            >
              <h2 className="font-bold">Contact Sales</h2>
            </div>
          </div>
        </div>
        <CommonFooter />
      </div>
    );
  }
}

SupportPage.propTypes = {
  isLoggedIn: PropTypes.bool,
};

SupportPage.defaultProps = {
  isLoggedIn: false,
};

export default SupportPage;
