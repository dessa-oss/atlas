import React from 'react';
import PropTypes from 'prop-types';

class CommonFooter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.onClickPolicies = this.onClickPolicies.bind(this);
  }

  onClickPolicies() {
    window.location = 'https://dessa.com/policies/';
  }

  render() {
    return (
      <div className="common-footer">
        <p>
          © 2020 Square, Inc. ATLAS, DESSA, the Dessa Logo, and others are trademarks of Square, Inc. All third party names and trademarks are properties of their respective owners and are used for identification purposes only.
        </p>
        <p>
          TensorFlow, the TensorFlow logo and any related marks are trademarks of Google Inc.
          RAPIDS, the RAPIDS logo and any related marks are trademarks and/or registered trademarks of NVIDIA
          Corporation.
        </p>
        <p>
          Microsoft Azure, the Microsoft Azure logo and any related marks are trademarks and/or registered trademarks
          of Microsoft Corporation.
          Google Cloud Platform, the Google Cloud Platform logo and any related marks are trademarks and/or registered
          trademarks of Google Inc.
        </p>
      </div>
    );
  }
}

CommonFooter.propTypes = {
};

CommonFooter.defaultProps = {
};

export default CommonFooter;
