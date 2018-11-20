import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import SelectColumnFilter from './filters/SelectColumnFilter';

class TableSectionHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleShowingFilter = this.toggleShowingFilter.bind(this);
    this.formatColumns = this.formatColumns.bind(this);
    this.state = {
      header: this.props.header,
      isShowingFilter: false,
      changeHiddenParams: this.props.changeHiddenParams,
      columns: this.props.columns,
    };
  }

  componentWillReceiveProps(nextProps) {
    const formatedColumns = this.formatColumns(nextProps.columns);
    this.setState({ columns: formatedColumns });
  }

  toggleShowingFilter() {
    const { isShowingFilter } = this.state;
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  formatColumns(columns) {
    const formatedColumns = [];

    if (columns !== null) {
      columns.forEach((col) => {
        formatedColumns.push({ name: col, hidden: false });
      });
    }
    return formatedColumns;
  }

  render() {
    const {
      header, isShowingFilter, changeHiddenParams, columns,
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
};

TableSectionHeader.defaultProps = {
  header: '',
  isShowingFilter: false,
  changeHiddenParams: () => {},
  columns: [],
};

export default TableSectionHeader;
