import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../../actions/CommonActions';

class ContainsFilter extends Component {
  constructor(props) {
    super(props);
    this.changeLocalParams = this.changeLocalParams.bind(this);
    this.onApply = this.onApply.bind(this);
    this.onCancel = this.onCancel.bind(this);
    this.onClearFilters = this.onClearFilters.bind(this);
    this.isDisabled = this.isDisabled.bind(this);
    this.state = {
      changeHiddenParams: this.props.changeHiddenParams,
      toggleShowingFilter: this.props.toggleShowingFilter,
      filterString: this.props.filterString,
      columnName: this.props.columnName,
      metricClass: this.props.metricClass,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        filterString: nextProps.filterString,
        columnName: nextProps.columnName,
        metricClass: nextProps.metricClass,
      },
    );
  }

  onApply() {
    const {
      changeHiddenParams, toggleShowingFilter, filterString, columnName,
    } = this.state;
    if (!this.isDisabled()) {
      changeHiddenParams(filterString, columnName);
      toggleShowingFilter();
    }
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

  isDisabled() {
    const { filterString } = this.state;
    return filterString.length === 0;
  }

  render() {
    const { filterString, metricClass } = this.state;

    const divClass = 'filter-container column-filter-container elevation-1 job-id-filter-container '
      .concat(metricClass);

    const applyClass = CommonActions.getApplyClass(this.isDisabled);

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
        <input type="text" onChange={(e) => { this.changeLocalParams(e); }} value={filterString} />
        <div className="column-filter-buttons">
          <button type="button" onClick={this.onCancel} className="b--mat b--negation text-upper">Cancel</button>
          <button type="button" onClick={this.onApply} className={applyClass}>Apply</button>
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
