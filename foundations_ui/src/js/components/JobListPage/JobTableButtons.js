import React, { Component } from 'react';
import PropTypes from 'prop-types';
import SelectColumnFilter from '../common/filters/SelectColumnFilter';
import BaseActions from '../../actions/BaseActions';

class JobTableButtons extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShowingFilter: false,
      columns: this.props.columns,
      updateSearchText: this.props.updateSearchText,
      hiddenColumns: this.props.hiddenColumns,
      updateHiddenColumns: this.props.updateHiddenColumns,
      selectedJobs: this.props.selectedJobs,
      projectName: this.props.projectName,
      getJobs: this.props.getJobs,
      selectNoJobs: this.props.selectNoJobs,
    };
    this.toggleShowingFilter = this.toggleShowingFilter.bind(this);
    this.onDeleteJobs = this.onDeleteJobs.bind(this);
    this.onClickTensor = this.onClickTensor.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        columns: nextProps.columns,
        hiddenColumns: nextProps.hiddenColumns,
        selectedJobs: nextProps.selectedJobs,
        projectName: nextProps.projectName,
      },
    );
  }

  toggleShowingFilter() {
    const { isShowingFilter } = this.state;
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  async onDeleteJobs() {
    const {
      selectedJobs, projectName, getJobs, selectNoJobs,
    } = this.state;
    if (selectedJobs.length > 0) {
      await selectedJobs.forEach(async (job) => {
        const URL = 'projects/'.concat(projectName).concat('/job_listing/').concat(job);
        await BaseActions.delAPIary(URL);
      });
      selectNoJobs();
      getJobs();
    }
  }

  async onClickTensor() {
    const {
      selectedJobs,
    } = this.state;
    const URL = 'generate_tensorboard';
    const res = await BaseActions.postApiary(URL, { job_ids: selectedJobs });
    window.open('https://www.google.ca', '_blank');
  }

  render() {
    const {
      isShowingFilter, columns, updateSearchText, hiddenColumns, updateHiddenColumns,
    } = this.state;
    let filter = null;
    if (isShowingFilter) {
      filter = (
        <SelectColumnFilter
          changeHiddenParams={updateHiddenColumns}
          columns={columns}
          toggleShowingFilter={this.toggleShowingFilter}
          hiddenInputParams={hiddenColumns}
          updateSearchText={updateSearchText}
        />
      );
    }

    return (
      <div className="job-details-header">
        <button
          onClick={this.onClickTensor}
          type="button"
        >
          <span className="i--icon-tf" /> <p className="text-upper">Send to tensorboard</p>
        </button>
        <button onClick={this.onDeleteJobs} type="button" className="text-upper">Delete</button>
        <div
          className="job-details-filter-button"
          role="button"
          tabIndex="0"
          onKeyPress={this.toggleShowingFilter}
          onClick={this.toggleShowingFilter}
        >
          <p>Filter Columns</p>
        </div>
        <div className="job-details-filter-container">
          {filter}
        </div>
      </div>
    );
  }
}

JobTableButtons.propTypes = {
  columns: PropTypes.array,
  updateSearchText: PropTypes.func,
  hiddenColumns: PropTypes.array,
  updateHiddenColumns: PropTypes.func,
  selectedJobs: PropTypes.array,
  projectName: PropTypes.string,
  getJobs: PropTypes.array,
  selectNoJobs: PropTypes.func,
};

JobTableButtons.defaultProps = {
  columns: [],
  updateSearchText: () => {},
  hiddenColumns: [],
  updateHiddenColumns: () => {},
  selectedJobs: [],
  projectName: '',
  getJobs: () => {},
  selectNoJobs: () => {},
};

export default JobTableButtons;
