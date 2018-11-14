import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactResizeDetector from 'react-resize-detector';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.onResize = this.onResize.bind(this);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      sizeCallback: this.props.sizeCallback,
      colIndex: this.props.colIndex,
    };
  }

  onResize(width, height) {
    const { sizeCallback, colIndex } = this.state;
    const { clientWidth } = this.headerContainer;
    sizeCallback(colIndex, clientWidth);
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
      <div
        className={containerDivClass}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4 className={headerClassName}>{title}</h4>
          <div className={arrowClassName} />
        </div>
        <ReactResizeDetector handleWidth handleHeight onResize={this.onResize} />
      </div>
    );
  }
}

JobColumnHeader.propTypes = {
  title: PropTypes.string,
  isStatus: PropTypes.number,
  className: PropTypes.string,
  containerClass: PropTypes.string,
  sizeCallback: PropTypes.func,
  colIndex: PropTypes.number,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: 0,
  className: '',
  containerClass: 'job-column-header',
  sizeCallback: () => null,
  colIndex: 0,
};

export default JobColumnHeader;
