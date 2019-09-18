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
      reload: this.props.reload,
    };
    this.toggleShowingFilter = this.toggleShowingFilter.bind(this);
    this.onDeleteJobs = this.onDeleteJobs.bind(this);
    this.onClickTensor = this.onClickTensor.bind(this);
    this.onClickRefresh = this.onClickRefresh.bind(this);
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
    const URL = 'upload_to_tensorboard';
    const resp = await BaseActions.postStaging(URL, { job_ids: selectedJobs });
    window.open(resp.url, resp.url);
  }

  async onClickRefresh() {
    const { reload } = this.props;
    reload();
  }


  render() {
    const {
      isShowingFilter, columns, updateSearchText, hiddenColumns, updateHiddenColumns, reload,
    } = this.state;
    const {
      buttonTensorboardEnabled,
    } = this.props;
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

    const buttonTensorboardDisabled = !buttonTensorboardEnabled;
    const iconClassName = buttonTensorboardDisabled ? 'i--icon-tf-disabled' : 'i--icon-tf';

    return (
      <div className="job-details-header">
        <button
          onClick={this.onClickRefresh}
          type="button"
        >
          <span className="i--icon-refresh"> <p className="text-upper font-bold">Refresh Table</p></span>
        </button>
        <button
          onClick={this.onClickTensor}
          type="button"
          disabled={buttonTensorboardDisabled}
          className={buttonTensorboardDisabled && 'disabled'}
        >
          <span className={iconClassName} /> <p className="text-upper">Send to tensorboard</p>
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
          <i className="i--icon-arrow-down" />
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
  reload: PropTypes.func,
  buttonTensorboardEnabled: PropTypes.bool,
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
  reload: () => {},
  buttonTensorboardEnabled: false,
};

export default JobTableButtons;
