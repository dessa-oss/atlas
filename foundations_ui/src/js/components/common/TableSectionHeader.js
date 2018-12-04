import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import SelectColumnFilter from './filters/SelectColumnFilter';

class TableSectionHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleShowingFilter = this.toggleShowingFilter.bind(this);
    this.state = {
      header: this.props.header,
      isShowingFilter: false,
      changeHiddenParams: this.props.changeHiddenParams,
      columns: this.props.columns,
      hiddenInputParams: this.props.hiddenInputParams,
      updateSearchText: this.props.updateSearchText,
      isMetric: this.props.isMetric,
    };
  }

  componentWillReceiveProps(nextProps) {
    const formatedColumns = this.formatColumns(nextProps.columns, nextProps.hiddenInputParams, nextProps.searchText);
    this.setState(
      { columns: formatedColumns, hiddenInputParams: nextProps.hiddenInputParams },
    );
  }

  toggleShowingFilter() {
    const { isShowingFilter, updateSearchText } = this.state;
    updateSearchText('');
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  formatColumns(columns, hiddenInputParams, searchText) {
    return CommonActions.formatColumns(columns, hiddenInputParams, searchText);
  }

  render() {
    const {
      header, isShowingFilter, changeHiddenParams, columns, hiddenInputParams, updateSearchText, isMetric,
    } = this.state;

    const divClass = CommonActions.getTableSectionHeaderDiv(header);
    const arrowClass = CommonActions.getTableSectionHeaderArrow(header);
    const textClass = CommonActions.getTableSectionHeaderText(header);

    let filter = null;
    if (isShowingFilter) {
      filter = (
        <SelectColumnFilter
          changeHiddenParams={changeHiddenParams}
          columns={columns}
          toggleShowingFilter={this.toggleShowingFilter}
          hiddenInputParams={hiddenInputParams}
          updateSearchText={updateSearchText}
        />
      );
    }

    return (
      <div className={divClass}>
        <p className={textClass}>{header}</p>
        <div
          role="presentation"
          onClick={this.toggleShowingFilter}
          onKeyPress={this.toggleShowingFilter}
          className="arrow-container"
        >
          <div className={arrowClass} />
        </div>
        {filter}
      </div>
    );
  }
}

TableSectionHeader.propTypes = {
  header: PropTypes.string,
  isShowingFilter: PropTypes.bool,
  changeHiddenParams: PropTypes.func,
  columns: PropTypes.array,
  hiddenInputParams: PropTypes.array,
  updateSearchText: PropTypes.func,
  searchText: PropTypes.string,
  isMetric: PropTypes.bool,
};

TableSectionHeader.defaultProps = {
  header: '',
  isShowingFilter: false,
  changeHiddenParams: () => {},
  columns: [],
  hiddenInputParams: [],
  updateSearchText: () => {},
  searchText: '',
  isMetric: false,
};

export default TableSectionHeader;
