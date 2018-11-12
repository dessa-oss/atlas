import React, { Component } from 'react';
import PropTypes from 'prop-types';


class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
    };
  }

  render() {
    const { title, isStatus } = this.state;
    let headerClassName = 'header-4 blue-border-bottom';
    let arrowClassName = 'arrow-down float-right';
    if (isStatus === 1) {
      headerClassName = 'header-4 blue-border-bottom status-header';
      arrowClassName = 'arrow-down margin-auto';
    }

    return (
      <div className="job-column-header">
        <h4 className={headerClassName}>{title}</h4>
        <div className={arrowClassName} />
      </div>
    );
  }
}

JobColumnHeader.propTypes = {
  title: PropTypes.string,
  isStatus: PropTypes.number,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: 0,
};

export default JobColumnHeader;
