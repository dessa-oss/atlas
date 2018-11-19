import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class TableSectionHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      header: this.props.header,
    };
  }

  render() {
    const { header } = this.state;
    const divClass = CommonActions.getTableSectionHeaderDiv(header);
    const arrowClass = CommonActions.getTableSectionHeaderArrow(header);
    const textClass = CommonActions.getTableSectionHeaderText(header);

    return (
      <div className={divClass}>
        <p className={textClass}>{header}</p>
        <div className={arrowClass} />
      </div>
    );
  }
}

TableSectionHeader.propTypes = {
  header: PropTypes.string,
};

TableSectionHeader.defaultProps = {
  header: '',
};

export default TableSectionHeader;
