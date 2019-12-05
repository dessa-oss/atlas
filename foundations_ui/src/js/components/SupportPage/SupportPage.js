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
          <div className="support-container">
            <h1>How can we help?</h1>
            <div>
              <h2 className="font-bold">Got a technical question?</h2>
              <p>Our Engineers are very active on <a href="https://www.stackoverflow.com/" target="blank">Stack Overflow</a> and constantly monitoring the 
                <span className="font-bold"> &quot;foundations-atlas&quot; tag, </span>
                help build the community by asking the question publicly.
              </p>
            </div>
            <div>
              <h2 className="font-bold">Need immediate help?</h2>
              <p>If you don&apos;t find what you&apos;re looking for in our documentation or StackOverflow, you can reach out to us via e-mail at <a href="mailto:foundations@dessa.com" target="blank">foundations@dessa.com</a>
              </p>
            </div>
            <div>
              <h2 className="font-bold">Foundations f or Enterprise?</h2>
              <p>Love using Foundations? Want to implement it for your team? Or want to learn more about what Enterprise
                version has to offer? Get in touch with us at <a href="mailto:deploy@dessa.com" target="blank">deploy@dessa.com</a>
              </p>
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
