import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../actions/JobListActions';
import Tooltip from './Tooltip';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseLeave = this.onMouseLeave.bind(this);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      toggleFilter: this.props.toggleFilter,
      isShowingTooltip: true,
    };
  }

  onMouseEnter() {
    this.setState({ isShowingTooltip: true });
  }

  onMouseLeave() {
    this.setState({ isShowingTooltip: true });
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter, isShowingTooltip,
    } = this.state;
    const headerClassName = JobActions.getJobColumnHeaderH4Class(isStatus);
    const arrowClassName = JobActions.getJobColumnHeaderArrowClass(isStatus);

    let tooltip = null;
    if (isShowingTooltip) {
      tooltip = <Tooltip message={title} />;
    }

    return (
      <div
        className={containerDivClass}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4
            onMouseEnter={this.onMouseEnter}
            onMouseLeave={this.onMouseLeave}
            className={headerClassName}
          >
            {title}{tooltip}
          </h4>
          <div className="icon-container" />
          <div role="presentation" onClick={toggleFilter} onKeyPress={toggleFilter} className="arrow-container">
            <div className={arrowClassName} />
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
  isShowingTooltip: PropTypes.bool,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
  isShowingTooltip: false,
};

export default JobColumnHeader;
