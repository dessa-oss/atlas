/* eslint-disable react/no-string-refs */
import React, { Component } from 'react';
import Select from 'react-select';
import PropTypes from 'prop-types';
import Plot from 'react-plotly.js';
import EmptyGraphImage from '../../../assets/svgs/empty-graph.svg';

class JobOverviewGraph extends Component {
  constructor(props) {
    super(props);
    this.onChangeMetric = this.onChangeMetric.bind(this);
  }

  onChangeMetric(selectedOption) {
    const { setMetric } = this.props;
    if (selectedOption && selectedOption.length > 0) {
      const metrics = selectedOption.map(m => m.value);
      setMetric(metrics);
    } else {
      setMetric(null);
    }
  }

  render() {
    const {
      allMetrics, jobIDs, graphData,
    } = this.props;

    const data = [...graphData].map(metric => {
      const x = [];
      const y = [];
      metric.values.forEach(job => {
        x.push(job[0]);
        y.push(job[1]);
      });
      return { x: x, y: y, name: metric.metric_name };
    });

    const layout = {
      xaxis: {
        categoryarray: jobIDs,
        categoryorder: 'array',
        title: {
          text: 'Job ID',
        },
        showticklabels: false,
      },
      yaxis: {
        title: {
          text: 'Values',
        },
      },
      showlegend: false,
      autosize: true,
    };

    const config = {
      displayModeBar: false,
    };

    const metricOptions = [];
    allMetrics.forEach(metricName => {
      metricOptions.push({ value: metricName, label: metricName });
    });

    const failedConversionMessage = <p className="not-graphable-message">This metric cannot be graphed.</p>;

    let chart = failedConversionMessage;
    if (metricOptions.length === 0) {
      chart = (
        <div className="empty-graph-block">
          <h4>No metrics have been logged yet!</h4>
          <img alt="" className="empty-graph-image" src={EmptyGraphImage} />
        </div>
      );
    } else {
      chart = <Plot data={data} layout={layout} config={config} useResizeHandler />;
    }

    return (
      <div>
        <div className="chart section-container">
          <h3 className="section-title">Recent Jobs</h3>
          <Select
            onChange={this.onChangeMetric}
            options={metricOptions}
            placeholder="Metrics"
            className="react-select"
            isMulti
          />
          <div className="plotly-chart">
            {chart}
          </div>
        </div>
      </div>
    );
  }
}

JobOverviewGraph.propTypes = {
  graphData: PropTypes.array,
  allMetrics: PropTypes.array,
  setMetric: PropTypes.func,
  jobIDs: PropTypes.array,
};

JobOverviewGraph.defaultProps = {
  graphData: [],
  allMetrics: [],
  setMetric: () => {},
  jobIDs: [],
};

export default JobOverviewGraph;
