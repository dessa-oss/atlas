import React, { Component } from 'react';
import PropTypes from 'prop-types';


class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
    };
  }

  render() {
    const { title, isStatus, offsetDivClass } = this.state;
    let headerClassName = 'header-4 blue-border-bottom';
    let arrowClassName = 'arrow-down float-right';
    if (isStatus === 1) {
      headerClassName = 'header-4 blue-border-bottom status-header';
      arrowClassName = 'arrow-down margin-auto';
    }

    return (
      <div className="job-column-header">
        <div className={offsetDivClass}>
          <h4 className={headerClassName}>{title}</h4>
          <div className={arrowClassName} />
        </div>
      </div>
    );
  }
}

JobColumnHeader.propTypes = {
  title: PropTypes.string,
  isStatus: PropTypes.number,
  className: PropTypes.string,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: 0,
  className: '',
};

export default JobColumnHeader;
