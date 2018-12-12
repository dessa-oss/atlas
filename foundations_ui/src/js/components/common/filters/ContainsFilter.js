import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ContainsFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      filterString: '',
      columnName: this.props.columnName,
      metricClass: this.props.metricClass,
    };
  }


  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, filterString, columnName,
    } = this.state;
    changeHiddenParams(filterString, columnName);
    toggleShowingFilter();
  }

  onCancel() {
    const { toggleShowingFilter } = this.state;
    toggleShowingFilter();
  }

  onClearFilters() {
    this.setState({ filterString: '' });
  }

  changeLocalParams(e) {
    this.setState({ filterString: e.target.value });
  }

  render() {
    const { filterString, metricClass, columnName } = this.state;

    const divClass = 'filter-container column-filter-container elevation-1 job-id-filter-container '
      .concat(metricClass);

    return (
      <div className={divClass}>
        <div className="column-filter-header">
          <p>contains</p>
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper float-right"
          >
          Clear Filters
          </button>
        </div>
        <input onChange={(e) => { this.changeLocalParams(e); }} value={filterString} />
        <p className="subtitle">Separate each keyword with a comma (i.e. “demo”, “job”)</p>
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className="b--mat b--affirmative text-upper">Apply</button>
        </div>
      </div>
    );
  }
}

ContainsFilter.propTypes = {
  changeHiddenParams: PropTypes.func,
  toggleShowingFilter: PropTypes.func,
  filterString: PropTypes.string,
  columnName: PropTypes.string,
  metricClass: PropTypes.string,
};

ContainsFilter.defaultProps = {
  changeHiddenParams: () => {},
  toggleShowingFilter: () => {},
  filterString: '',
  columnName: '',
  metricClass: 'not-metric',
};

export default ContainsFilter;
