import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

class JobOverviewGraph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      metric: this.props.metric,
    };
  }

  render() {
    const { metric } = this.state;
    const options = {
      chart: {
        type: 'spline',
      },
      xAxis: {
        type: 'datetime',
        title: {
          text: 'Date',
        },
        dateTimeLabelFormats: {
          day: '%e. %b',
          month: '%b \'%y',
          year: '%Y',
        },
      },
      yAxis: {
        title: {
          text: metric,
        },
      },
      title: {
        text: '',
      },
      series: [
        {
          showInLegend: false,
          data: [[Date.UTC(2019, 1, 1), 1], [Date.UTC(2019, 2, 1), 3], [Date.UTC(2019, 4, 1), 8],
            [Date.UTC(2019, 5, 1), 3], [Date.UTC(2019, 5, 29), 8], [Date.UTC(2019, 6, 1), 2],
            [Date.UTC(2019, 7, 1), 5], [Date.UTC(2019, 8, 1), 4], [Date.UTC(2019, 9, 1), 12],
            [Date.UTC(2019, 10, 1), 6], [Date.UTC(2019, 11, 1), 6], [Date.UTC(2019, 12, 1), 0],
          ],
        },
        {
          showInLegend: false,
          data: [[Date.UTC(2019, 1, 1), 4], [Date.UTC(2019, 1, 15), 6], [Date.UTC(2019, 2, 1), 5],
            [Date.UTC(2019, 4, 1), 2], [Date.UTC(2019, 5, 1), 13], [Date.UTC(2019, 6, 1), 4],
            [Date.UTC(2019, 7, 1), 5], [Date.UTC(2019, 8, 1), 12], [Date.UTC(2019, 9, 1), 4],
            [Date.UTC(2019, 10, 1), 9], [Date.UTC(2019, 11, 1), 4], [Date.UTC(2019, 12, 1), 1],
          ],
        },
        {
          showInLegend: false,
          data: [[Date.UTC(2019, 1, 1), 9], [Date.UTC(2019, 2, 1), 7], [Date.UTC(2019, 4, 1), 7],
            [Date.UTC(2019, 5, 1), 6], [Date.UTC(2019, 6, 1), 8], [Date.UTC(2019, 6, 14), 1],
            [Date.UTC(2019, 7, 1), 3], [Date.UTC(2019, 8, 1), 8], [Date.UTC(2019, 9, 1), 2],
            [Date.UTC(2019, 10, 1), 3], [Date.UTC(2019, 11, 1), 8], [Date.UTC(2019, 12, 1), 2],
          ],
        },
      ],
    };

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
        <div>
          <HighchartsReact highcharts={Highcharts} options={options} />
        </div>
      </div>
    );
  }
}

JobOverviewGraph.propTypes = {
  metric: PropTypes.string,
};

JobOverviewGraph.defaultProps = {
  metric: 'metric',
};

export default JobOverviewGraph;
