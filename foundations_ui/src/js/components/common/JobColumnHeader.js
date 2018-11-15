import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../actions/JobListActions';

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
    const headerClassName = JobActions.getJobColumnHeaderH4Class(isStatus);
    const arrowClassName = JobActions.getJobColumnHeaderArrowClass(isStatus);

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
  isStatus: PropTypes.bool,
  className: PropTypes.string,
  containerClass: PropTypes.string,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
};

export default JobColumnHeader;
