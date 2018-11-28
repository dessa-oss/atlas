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
      unsetClearFilters: this.props.unsetClearFilters,
      statusCircle: this.props.statusCircle,
    };
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.showAllFilters) {
      this.setState({ hidden: false });
    }
  }

  onChange() {
    const {
      hidden, changeHiddenParams, name, unsetClearFilters,
    } = this.state;
    this.setState({ hidden: !hidden });
    changeHiddenParams(name);
    unsetClearFilters();
  }

  render() {
    const { name, hidden, statusCircle } = this.state;

    const id = name.concat('-checkbox');

    let circle = '';
    if (statusCircle !== null) {
      circle = <span className={statusCircle} />;
    }

    return (
      <div className="checkbox-container">
        <div className="custom-checkbox">
          <label htmlFor={id} className="control control--checkbox">
            <input id={id} checked={!hidden} onChange={this.onChange} type="checkbox" />
            <div className="control__indicator" />
          </label>
        </div>
        <div className="checkbox-value">
          {circle}
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
  showAllFilters: PropTypes.bool,
  unsetClearFilters: PropTypes.func,
  statusCircle: PropTypes.string,
};

Checkbox.defaultProps = {
  name: '',
  hidden: false,
  changeHiddenParams: () => {},
  showAllFilters: false,
  unsetClearFilters: () => {},
  statusCircle: null,
};

export default Checkbox;
