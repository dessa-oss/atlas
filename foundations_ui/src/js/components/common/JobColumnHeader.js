import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
    };
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass,
    } = this.state;
    let headerClassName = 'header-4 blue-border-bottom';
    let arrowClassName = 'arrow-down float-right';
    if (isStatus === 1) {
      headerClassName = 'header-4 blue-border-bottom status-header';
      arrowClassName = 'arrow-down margin-auto';
    }

    return (
      <div className={containerDivClass}>
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
  containerClass: PropTypes.string,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: 0,
  className: '',
  containerClass: 'job-column-header',
};

export default JobColumnHeader;
