import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Checkbox extends Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
    this.state = {
      name: this.props.name,
      hidden: this.props.hidden,
      changeHiddenParams: this.props.changeHiddenParams,
    };
  }

  onChange() {
    const { hidden, changeHiddenParams, name } = this.state;
    console.log('onchange');
    this.setState({ hidden: !hidden });
    changeHiddenParams(name);
  }

  render() {
    const { name, hidden } = this.state;

    const id = name.concat('-checkbox');

    return (
      <div className="checkbox-container">
        <div className="custom-checkbox">
          <label htmlFor={id} className="control control--checkbox">
            <input id={id} checked={!hidden} onChange={this.onChange} type="checkbox" />
            <div className="control__indicator" />
          </label>
        </div>
        <div className="checkbox-value">
          <h5>{name}</h5>
        </div>
      </div>
    );
  }
}

Checkbox.propTypes = {
  name: PropTypes.string,
  hidden: PropTypes.bool,
  changeHiddenParams: PropTypes.func,
};

Checkbox.defaultProps = {
  name: '',
  hidden: false,
  changeHiddenParams: () => {},
};

export default Checkbox;
