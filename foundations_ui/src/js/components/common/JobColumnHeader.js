import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobListActions from '../../actions/JobListActions';
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
      isFiltered: this.props.isFiltered,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        isFiltered: nextProps.isFiltered,
      },
    );
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter, colType, isMetric, isFiltered,
    } = this.state;
    const headerClassName = JobListActions.getJobColumnHeaderH4Class(isStatus);
    const arrowClassName = JobListActions.getJobColumnHeaderArrowClass(isStatus, colType, isMetric);
    let divClassName = JobListActions.getJobColumnHeaderDivClass(containerDivClass, isStatus);

    if (title === 'Tags') {
      divClassName = 'job-column-header job-cell tag-cell';
    }

    const presentationClassName = JobListActions.getJobColumnHeaderPresentationClass(colType, isMetric);

    const tooltip = <Tooltip message={title} />;
    const filterIcon = isFiltered ? <div className="i--icon-filtered" /> : null;

    return (
      <div
        className={`${divClassName} ${title}`}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4 className={`${headerClassName}`}>
            {title}
          </h4>
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
  isFiltered: PropTypes.bool,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
  colType: 'string',
  isMetric: false,
  isFiltered: false,
};

export default JobColumnHeader;
