import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Toolbar from '../common/Toolbar';
import Header from '../common/Header';

class ContactPage extends Component {
  render() {
    const contactBanner = 'Contact us';
    const contactSubtext = 'Get in touch, we are here to help';

    return (
      <div className="contact-page-container">
        <div className="header">
          <Toolbar />
          <h1 className="text-blue text-center">{contactBanner}</h1>
          <p className="text-blue text-center">{contactSubtext}</p>
          <div className="ctaWrapper">
            <div className="ctaElement">
              <h3>Sales</h3>
              <p>See how data scientists in your company
                can benefit from the productivity boost
                <strong> Foundations</strong> provides? Let us get you sorted.
              </p>
              <button type="button"><a href="mailto:foundations@dessa.com">Contact Sales</a></button>
            </div>
            <div className="ctaElement">
              <h3>Help & Support</h3>
              <p>Facing a difficulty with code or have any other questions? We are here to help.</p>
              <button type="button"><a href="mailto:support@dessa.com"> Contact Engineers</a></button>
            </div>
            <div className="ctaElement">
              <h3>Sales</h3>
              <p>For all other general inquiries, reach out to <a href="mailto:info@dessa.com">info@dessa.com</a></p>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ContactPage;
