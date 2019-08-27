import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactTooltip from 'react-tooltip';
import JobListActions from '../../actions/JobListActions';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.onClickSortAsc = this.onClickSortAsc.bind(this);
    this.onClickSortDesc = this.onClickSortDesc.bind(this);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      toggleFilter: this.props.toggleFilter,
      colType: this.props.colType,
      isMetric: this.props.isMetric,
      isFiltered: this.props.isFiltered,
      isSortedColumn: this.props.isSortedColumn,
      isAscending: this.props.isAscending,
      sortTable: this.props.sortTable,
      selectAllJobs: this.props.selectAllJobs,
      allJobsSelected: this.props.allJobsSelected,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        title: nextProps.title,
        isFiltered: nextProps.isFiltered,
        isSortedColumn: nextProps.isSortedColumn,
        isAscending: nextProps.isAscending,
        allJobsSelected: nextProps.allJobsSelected,
      },
    );
  }

  onClickSortAsc() {
    const { sortTable, title } = this.state;

    sortTable(title, true);
  }

  onClickSortDesc() {
    const { sortTable, title } = this.state;

    sortTable(title, false);
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter, colType, isMetric, isFiltered, isSortedColumn,
      isAscending, selectAllJobs, allJobsSelected,
    } = this.state;
    const headerClassName = JobListActions.getJobColumnHeaderH4Class(isStatus);
    let divClassName = JobListActions.getJobColumnHeaderDivClass(containerDivClass, isStatus);

    let headerName = title;

    if (title === 'Tags') {
      divClassName = 'job-column-header job-cell tag-cell';
    }

    if (title === 'SelectAllCheckboxes') {
      headerName = <input type="checkbox" checked={allJobsSelected} onClick={() => { selectAllJobs(); }} />;
    }

    let arrowUp = null;
    let arrowDown = null;
    if (title !== '' && title.toLowerCase() !== 'job id' && title.toLowerCase() !== 'tags') {
      arrowUp = (
        <i
          onKeyPress={this.onClickSortAsc}
          tabIndex={0}
          role="button"
          onClick={this.onClickSortAsc}
          className={isSortedColumn && (isAscending === null || isAscending)
            ? 'i--icon-arrow-up' : 'i--icon-arrow-up-unfilled'}
        />
      );
      arrowDown = (
        <i
          onKeyPress={this.onClickSortDesc}
          tabIndex={0}
          role="button"
          onClick={this.onClickSortDesc}
          className={isSortedColumn && (isAscending === null || !isAscending)
            ? 'i--icon-arrow-down' : 'i--icon-arrow-down-unfilled'}
        />
      );
    }

    return (
      <div
        className={`${divClassName} ${title}`}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4 className={`${headerClassName}`} data-tip={title.length > 15 ? headerName : ''}>
            {headerName}
            <ReactTooltip place="top" type="dark" effect="solid" />
          </h4>
          {arrowUp}
          {arrowDown}
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
  isSortedColumn: PropTypes.bool,
  isAscending: PropTypes.bool,
  sortTable: PropTypes.func,
  selectAllJobs: PropTypes.func,
  allJobsSelected: PropTypes.bool,
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
  isSortedColumn: false,
  isAscending: false,
  sortTable: () => {},
  selectAllJobs: () => {},
  allJobsSelected: false,
};

export default JobColumnHeader;
