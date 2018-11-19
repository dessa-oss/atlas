import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';
import SelectColumnFilter from './filters/SelectColumnFilter';

class TableSectionHeader extends Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
    this.state = {
      header: this.props.header,
      isShowingFilter: false,
    };
  }

  onClick() {
    const { isShowingFilter } = this.state;
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  render() {
    const { header, isShowingFilter } = this.state;
    const divClass = CommonActions.getTableSectionHeaderDiv(header);
    const arrowClass = CommonActions.getTableSectionHeaderArrow(header);
    const textClass = CommonActions.getTableSectionHeaderText(header);

    let filter = null;
    if (isShowingFilter) {
      filter = <SelectColumnFilter />;
    }

    return (
      <div className={divClass}>
        <p className={textClass}>{header}</p>
        <div role="presentation" onClick={this.onClick} onKeyPress={this.onClick} className="arrow-container">
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
};

TableSectionHeader.defaultProps = {
  header: '',
  isShowingFilter: false,
};

export default TableSectionHeader;
