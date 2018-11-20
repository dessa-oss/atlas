import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Checkbox from '../Checkbox';

class SelectColumnFilter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      columns: this.props.columns,
      changeHiddenParams: this.props.changeHiddenParams,
    };
  }

  render() {
    const { columns, changeHiddenParams } = this.state;

    let checkboxes = null;
    if (columns.length > 0) {
      checkboxes = [];
    }
    columns.forEach((col) => {
      const key = col.name.concat('-checkbox');
      checkboxes.push(<Checkbox
        key={key}
        name={col.name}
        hidden={col.hidden}
        changeHiddenParams={changeHiddenParams}
      />);
    });

    return (
      <div className="filter-container column-filter-container">
        <div className="column-filter-header">
          <input />
          <div className="mg-bg">
            <div className="magnifying-glass" />
          </div>
          <button type="button" className="b--mat b--affirmative text-upper float-right">Clear Filters</button>
        </div>
        <div className="column-filter-list">
          {checkboxes}
        </div>
        <div className="column-filter-buttons">
          <button type="button" className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

SelectColumnFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
};

SelectColumnFilter.defaultProps = {
  columns: [{ name: 'abc', hidden: false }, { name: '123', hidden: false }, { name: 'abc123', hidden: false }],
  changeHiddenParams: () => {},
};

export default SelectColumnFilter;
