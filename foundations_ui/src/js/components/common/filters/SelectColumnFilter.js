import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Checkbox from '../Checkbox';

const notFound = -1;
const oneElement = 1;

class SelectColumnFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.state = {
      columns: this.props.columns,
      changeHiddenParams: this.props.changeHiddenParams,
      changedParams: [],
      toggleShowingFilter: this.props.toggleShowingFilter,
    };
  }

  onApply() {
    const { changeHiddenParams, changedParams, toggleShowingFilter } = this.state;
    changeHiddenParams(changedParams);
    toggleShowingFilter();
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    toggleShowingFilter();
  }

  changeLocalParams(colName) {
    const { changedParams } = this.state;
    const index = changedParams.indexOf(colName);
    let newArray = [];
    if (index !== notFound) {
      changedParams.splice(index, oneElement);
    } else {
      changedParams.push(colName);
    }
    newArray = changedParams;
    this.setState({ changedParams: newArray });
  }

  render() {
    const { columns } = this.state;

    let checkboxes = null;
    if (columns.length > 0) {
      checkboxes = [];
      columns.forEach((col) => {
        const key = col.name.concat('-checkbox');
        checkboxes.push(<Checkbox
          key={key}
          name={col.name}
          hidden={col.hidden}
          changeHiddenParams={this.changeLocalParams}
        />);
      });
    }

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
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

SelectColumnFilter.propTypes = {
  columns: PropTypes.array,
  changeHiddenParams: PropTypes.func,
  changedParams: PropTypes.array,
  toggleShowingFilter: PropTypes.func,
};

SelectColumnFilter.defaultProps = {
  columns: [],
  changeHiddenParams: () => {},
  changedParams: [],
  toggleShowingFilter: () => {},
};

export default SelectColumnFilter;
