import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Checkbox from '../Checkbox';

class SelectColumnFilter extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    return (
      <div className="column-filter-container">
        <div className="column-filter-header">
          <input />
          <div className="i--search" />
          <button type="button" className="text-upper">Clear Filters</button>
        </div>
        <div className="column-filter-list">
          <Checkbox />
          <Checkbox />
          <Checkbox />
          <Checkbox />
          <Checkbox />
        </div>
        <div className="column-filter-buttons">
          <button type="button" className="text-upper">Cancel</button>
          <button type="button" className="text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

SelectColumnFilter.propTypes = {
};

SelectColumnFilter.defaultProps = {
};

export default SelectColumnFilter;
