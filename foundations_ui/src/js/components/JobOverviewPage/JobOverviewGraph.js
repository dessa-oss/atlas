import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobOverviewGraph extends Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  render() {
    return (
      <div className="chart section-container">
        <h3>Recent Jobs</h3>
        <select>
          <option selected="selected">
          Metrics
          </option>
        </select>
        <select>
          <option selected="selected">
          Sort by
          </option>
        </select>
      </div>
    );
  }
}

JobOverviewGraph.propTypes = {
};

JobOverviewGraph.defaultProps = {
};

export default JobOverviewGraph;
