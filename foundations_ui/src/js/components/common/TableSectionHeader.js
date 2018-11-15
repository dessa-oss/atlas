import React, { Component } from 'react';
import PropTypes from 'prop-types';

class TableSectionHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      header: this.props.header,
    };
  }

  render() {
    const { header } = this.state;
    let divClass = 'table-section-header';
    let arrowClass = '';
    let textClass = 'blue-header-text font-regular white-text no-margin';
    if (header !== '') {
      divClass = 'table-section-header blue-header';
      arrowClass = 'arrow-down blue-header-arrow border-top-white';
      textClass = 'blue-header-text font-regular white-text';
    }
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
