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
      colType: this.props.colType,
      isMetric: this.props.isMetric,
    };
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter, colType, isMetric,
    } = this.state;
    const headerClassName = JobActions.getJobColumnHeaderH4Class(isStatus);
    let arrowClassName = JobActions.getJobColumnHeaderArrowClass(isStatus);

    const tooltip = <Tooltip message={title} />;

    let divClass = containerDivClass;
    if (isStatus) {
      divClass += ' status-header';
    }

    let metricClass = 'not-metric';
    if (isMetric) {
      metricClass = 'is-metric';
    }

    arrowClassName = arrowClassName.concat(' ').concat(colType).concat(' ').concat(metricClass);
    const className = 'arrow-container '.concat(colType).concat(' ').concat(metricClass);

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
          <div role="presentation" onClick={toggleFilter} onKeyPress={toggleFilter} className={className}>
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
  colType: PropTypes.string,
  isMetric: PropTypes.bool,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
  colType: 'string',
  isMetric: false,
};

export default JobColumnHeader;
