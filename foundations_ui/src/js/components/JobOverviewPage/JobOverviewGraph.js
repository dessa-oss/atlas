/* eslint-disable react/no-string-refs */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

class JobOverviewGraph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      metric: this.props.metric,
      graphData: this.props.graphData,
      formattedGraphData: [],
      allMetrics: this.props.allMetrics,
      setMetric: this.props.setMetric,
    };

    this.formatGraphData = this.formatGraphData.bind(this);
    this.onChangeMetric = this.onChangeMetric.bind(this);
  }

  componentDidMount() {
    this.formatGraphData();
  }

  async componentWillReceiveProps(nextProps) {
    if (nextProps.metric) {
      await this.setState({ metric: nextProps.metric });
    }
    if (nextProps.graphData) {
      await this.setState({ graphData: nextProps.graphData });
      await this.formatGraphData();
    }
    this.setState({ allMetrics: nextProps.allMetrics });
  }

  formatGraphData() {
    const { graphData } = this.state;
    let graphCopy = [...graphData];
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
    let seriesArray = [];
    let seriesObject = {};
    seriesObject.showInLegend = false;
    seriesObject.data = graphCopy;
    seriesArray.push(seriesObject);

    if (seriesArray.length === 0) {
      seriesArray = [{ showInLegend: false, data: {} }];
    }

    this.setState({ formattedGraphData: seriesArray });
  }

  onChangeMetric(e) {
    const { setMetric } = this.state;
    const metric = e.target.value;
    setMetric(metric);
  }

  render() {
    const { metric, formattedGraphData, allMetrics } = this.state;

    const options = {
      chart: {
        type: 'spline',
      },
      xAxis: {
        type: 'category',
        title: {
          text: 'Job Id',
        },
        showEmpty: true,
      },
      yAxis: {
        title: {
          text: metric,
        },
        showEmpty: true,
      },
      title: {
        text: '',
      },
      series: formattedGraphData,
    };

    const metrics = [];
    metrics.push(<option key="Metrics" selected disabled hidden>Metrics</option>);
    allMetrics.forEach((metricName) => {
      metrics.push(<option key={metricName}>{metricName}</option>);
    });

    return (
      <div>
        <h3 className="section-title">Recent Jobs</h3>
        <div className="chart section-container">
          <select onChange={this.onChangeMetric}>
            {metrics}
          </select>
          <div className="highchart-chart">
            <HighchartsReact highcharts={Highcharts} options={options} />
          </div>
        </div>
      </div>
    );
  }
}

JobOverviewGraph.propTypes = {
  metric: PropTypes.string,
  graphData: PropTypes.array,
  allMetrics: PropTypes.array,
  setMetric: PropTypes.func,
};

JobOverviewGraph.defaultProps = {
  metric: '',
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
};

export default JobOverviewGraph;
