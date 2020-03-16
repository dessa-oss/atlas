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
      </div>
    );
  }
}

CommonFooter.propTypes = {
};

CommonFooter.defaultProps = {
};

export default CommonFooter;
