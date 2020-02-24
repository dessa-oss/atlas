/* eslint-disable react/no-string-refs */
import React, { Component } from 'react';
import Select from 'react-select';
import PropTypes from 'prop-types';
import Plot from 'react-plotly.js';
import EmptyGraphImage from '../../../assets/svgs/empty-graph.svg';

class JobOverviewGraph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      graphData: this.props.graphData,
      formattedGraphData: [],
      allMetrics: this.props.allMetrics,
      setMetric: this.props.setMetric,
      jobIDs: this.props.jobIDs,
      failedToConvert: false,
      // metricNames: [],
    };

    this.formatGraphData = this.formatGraphData.bind(this);
    this.formatGraphMetric = this.formatGraphMetric.bind(this);
    this.onChangeMetric = this.onChangeMetric.bind(this);
  }

  componentDidMount() {
    this.formatGraphData();
  }

  async componentWillReceiveProps(nextProps) {
    if (nextProps.graphData) {
      await this.setState({ graphData: nextProps.graphData });
      await this.formatGraphData();
    }
    this.setState({ allMetrics: nextProps.allMetrics, jobIDs: nextProps.jobIDs });
  }

  formatGraphData() {
    const { graphData } = this.state;
    const graphCopy = [...graphData];

    const allSeries = graphCopy.map(this.formatGraphMetric);
    this.setState({ formattedGraphData: allSeries });
    // this.setState({ metricNames: graphData.map(m => m.metric_name) });
  }

  formatGraphMetric(graphData) {
    const { jobIDs } = this.state;
    // Assumes the following format
    /*
    [
      [
        [Date Object like {2019, 04, 04}, value like 12],
        [...] more [date, value] pairs
      ],
      [
        Another graph's [date, value] pairs
      ],
      [...]
    ]
    */
    const seriesObject = {};
    seriesObject.showInLegend = false;
    seriesObject.marker = {
      symbol: 'circle',
      radius: 4,
    };
    seriesObject.name = graphData.metric_name;
    seriesObject.color = '#5480DC';
    // n^2 time, needs refactoring
    seriesObject.data = graphData.values.map(p => [jobIDs.length - jobIDs.indexOf(p[0]) - 1, p[1]]);

    return seriesObject;
  }

  onChangeMetric(selectedOption) {
    const { setMetric } = this.state;
    if (selectedOption && selectedOption.length > 0) {
      const metrics = selectedOption.map(m => m.value);
      setMetric(metrics);
    } else {
      setMetric(null);
    }
  }

  render() {
    const {
      formattedGraphData, allMetrics, failedToConvert, jobIDs, graphData,
    } = this.state;

    const data = graphData.map(metric => {
      const x = [];
      const y = [];
      metric.values.forEach(job => {
        x.push(job[0]);
        y.push(job[1]);
      });
      return { x: x, y: y };
    });

    const layout = {
      xaxis: {
        tickvals: jobIDs,
      },
    };

    console.log(layout);

    const options = {
      chart: {
        type: 'spline',
        parallelCoordinates: true,
        parallelAxes: {
          lineWidth: 2,
        },
      },
      xAxis: {
        categories: jobIDs,
        labels: {
          enabled: false,
        },
        title: {
          text: 'Job Id',
        },
        showEmpty: true,
      },
      title: {
        text: '',
      },
      series: formattedGraphData,
      tooltip: {
        crosshairs: {
          width: '3px',
        },
        shared: true,
      },
    };

    const metricOptions = [];
    allMetrics.forEach(metricName => {
      metricOptions.push({ value: metricName, label: metricName });
    });

    const failedConversionMessage = <p className="not-graphable-message">This metric cannot be graphed.</p>;

    let chart = failedConversionMessage;
    if (!failedToConvert) {
      if (metricOptions.length === 0) {
        chart = (
          <div className="empty-graph-block">
            <h4>No metrics have been logged yet!</h4>
            <img alt="" className="empty-graph-image" src={EmptyGraphImage} />
          </div>
        );
      } else {
        // chart = <HighchartsReact highcharts={Highcharts} options={options} />;
        chart = <Plot data={data} layout={layout} />;
      }
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
          <div className="highchart-chart">
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
  graphData: [
    [
      [Date.UTC(2019, 1, 1), 9], [Date.UTC(2019, 2, 1), 7], [Date.UTC(2019, 4, 1), 7],
      [Date.UTC(2019, 5, 1), 6], [Date.UTC(2019, 6, 1), 8], [Date.UTC(2019, 6, 14), 1],
      [Date.UTC(2019, 7, 1), 3], [Date.UTC(2019, 8, 1), 8], [Date.UTC(2019, 9, 1), 2],
      [Date.UTC(2019, 10, 1), 3], [Date.UTC(2019, 11, 1), 8], [Date.UTC(2019, 12, 1), 2],
    ],
    [
      [Date.UTC(2019, 1, 1), 1], [Date.UTC(2019, 2, 1), 3], [Date.UTC(2019, 4, 1), 8],
      [Date.UTC(2019, 5, 1), 3], [Date.UTC(2019, 5, 29), 8], [Date.UTC(2019, 6, 1), 2],
      [Date.UTC(2019, 7, 1), 5], [Date.UTC(2019, 8, 1), 4], [Date.UTC(2019, 9, 1), 12],
      [Date.UTC(2019, 10, 1), 6], [Date.UTC(2019, 11, 1), 6], [Date.UTC(2019, 12, 1), 0],
    ],
    [
      [Date.UTC(2019, 1, 1), 4], [Date.UTC(2019, 1, 15), 6], [Date.UTC(2019, 2, 1), 5],
      [Date.UTC(2019, 4, 1), 2], [Date.UTC(2019, 5, 1), 13], [Date.UTC(2019, 6, 1), 4],
      [Date.UTC(2019, 7, 1), 5], [Date.UTC(2019, 8, 1), 12], [Date.UTC(2019, 9, 1), 4],
      [Date.UTC(2019, 10, 1), 9], [Date.UTC(2019, 11, 1), 4], [Date.UTC(2019, 12, 1), 1],
    ],
  ],
  allMetrics: [],
  setMetric: () => {},
  jobIDs: [],
};

export default JobOverviewGraph;
