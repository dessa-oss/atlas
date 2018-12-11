import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../actions/JobListActions';
import Tooltip from './Tooltip';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      toggleFilter: this.props.toggleFilter,
    };
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter,
    } = this.state;
    const headerClassName = JobActions.getJobColumnHeaderH4Class(isStatus);
    const arrowClassName = JobActions.getJobColumnHeaderArrowClass(isStatus);

    const tooltip = <Tooltip message={title} />;

    let divClass = containerDivClass;
    if (isStatus) {
      divClass += ' status-header';
    }

    return (
      <div
        className={divClass}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4
            className={headerClassName}
          >
            {title}
          </h4>
          {tooltip}
          <div className="icon-container" />
          <div role="presentation" onClick={toggleFilter} onKeyPress={toggleFilter} className="arrow-container">
            <div id={title} className={arrowClassName} />
          </div>
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
  toggleFilter: PropTypes.func,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
};

export default JobColumnHeader;
