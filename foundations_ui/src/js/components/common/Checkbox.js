import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Checkbox extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    return (
      <div className="checkbox-container">
        <div className="custom-checkbox">
          <label htmlFor="abc" className="control control--checkbox">
            <input id="abc" type="checkbox" />
            <div className="control__indicator" />
          </label>
        </div>
        <div className="checkbox-value">
          <h5>Checkbox Text</h5>
        </div>
      </div>
    );
  }
}

Checkbox.propTypes = {
};

Checkbox.defaultProps = {
};

export default Checkbox;
