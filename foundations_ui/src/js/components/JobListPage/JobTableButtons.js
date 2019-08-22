import React, { Component } from 'react';
import PropTypes from 'prop-types';
import SelectColumnFilter from '../common/filters/SelectColumnFilter';

class JobTableButtons extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShowingFilter: false,
      columns: this.props.columns,
    };
    this.toggleShowingFilter = this.toggleShowingFilter.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        columns: nextProps.columns,
      },
    );
  }

  toggleShowingFilter() {
    const { isShowingFilter } = this.state;
    this.setState({ isShowingFilter: !isShowingFilter });
  }

  render() {
    const { isShowingFilter, columns } = this.state;
    let filter = null;
    if (isShowingFilter) {
      filter = (
        <SelectColumnFilter
          // changeHiddenParams={changeHiddenParams}
          columns={columns}
          toggleShowingFilter={this.toggleShowingFilter}
          // hiddenInputParams={hiddenInputParams}
          // updateSearchText={updateSearchText}
        />
      );
    }

    return (
      <div className="job-details-header">
        <button type="button"><span className="i--icon-tf" /> <p className="text-upper">Send to tensorboard</p></button>
        <button type="button" className="text-upper">Delete</button>
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
};

JobTableButtons.defaultProps = {
  columns: [],
};

export default JobTableButtons;
