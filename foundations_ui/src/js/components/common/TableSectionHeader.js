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
    };
  }

  componentWillReceiveProps(nextProps) {
    const formatedColumns = CommonActions.formatColumns(nextProps.columns, nextProps.hiddenInputParams);
    this.setState({ columns: formatedColumns });
  }

  toggleShowingFilter() {
    const { isShowingFilter } = this.state;
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  render() {
    const {
      header, isShowingFilter, changeHiddenParams, columns, hiddenInputParams,
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
};

TableSectionHeader.defaultProps = {
  header: '',
  isShowingFilter: false,
  changeHiddenParams: () => {},
  columns: [],
  hiddenInputParams: [],
};

export default TableSectionHeader;
