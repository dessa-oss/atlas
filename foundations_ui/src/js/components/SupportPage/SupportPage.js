/* eslint-disable max-len */
/* eslint-disable no-trailing-spaces */
import React, { Component } from 'react';
import CommonHeader from '../common/CommonHeader';
import CommonFooter from '../common/CommonFooter';

class SupportPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
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
    return (
      <div>
        <CommonHeader />
        <div className="support-page-container">
          <div>
            <h2 className="font-bold">Got a technical question?</h2>
            <p>Our Engineers are very active on StackOverflow and constantly monitoring the 
              <span className="font-bold"> &quot;foundations-atlas&quot; tag, </span>
              help build the community by asking the question publicly.
            </p>
            <div tabIndex={0} role="button" onKeyPress={this.onClickStackOverflow} onClick={this.onClickStackOverflow}>
              <h2 className="font-bold">Ask on StackOverflow</h2>
            </div>
          </div>
          <div>
            <h2 className="font-bold">Need immediate help?</h2>
            <p>If the documentation and StackOverflow weren&apos;t helpful you can reach out to us via e-mail at
              <span> </span>
              <span
                tabIndex={0}
                role="button"
                onKeyPress={this.onClickEmailUs}
                onClick={this.onClickEmailUs}
                className="underline"
              >
                 foundations@dessa.com
              </span>
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
              version has to offer? Get in touch with us at
              <span> </span>
              <span
                tabIndex={0}
                role="button"
                onKeyPress={this.onClickSales}
                onClick={this.onClickSales}
                className="underline"
              >
                deploy@dessa.com
              </span>
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

export default SupportPage;
