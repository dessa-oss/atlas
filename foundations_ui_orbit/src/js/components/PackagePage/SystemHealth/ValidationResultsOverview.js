import React, { Component } from "react";
import moment from "moment";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import Select from "react-select";
import PropTypes from "prop-types";

class ValidationResultsOverview extends Component {
  render() {
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");
    const sign = validationResult.row_count.row_count_diff >= 0 ? "+" : "-";
    const rowDiff = Math.round(Math.abs(validationResult.row_count.row_count_diff) * 1000) / 1000;
    const rowCount = `${validationResult.row_count.expected_row_count} -> ${validationResult.row_count.actual_row_count} (${sign}${rowDiff}%)`; // eslint-disable-line max-len

    const binLabels = ["10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90"];
    const series = [
      {
        name: "Expected Data",
        data: [5, 10, -1, 4, 19, 15, 2, 4]
      },
      {
        name: "Actual Data",
        data: [6, 13, 4, 2, 22, 13, 1, 6]
      }
    ];

    const options = {
      chart: {
        type: "column"
      },
      title: {
        text: ""
      },
      xAxis: {
        categories: binLabels,
        showEmpty: true,
        minPadding: 0,
        maxPadding: 0
      },
      yAxis: {
        lineWidth: 1,
        title: {
          text: "",
          allowDecimals: false
        }
      },
      legend: {
        enabled: false
      },
      tooltip: {
        formatter: function () {
          const expectedPoint = this.points[0];
          const actualPoint = this.points[1];
          const expectedTooltip = `${expectedPoint.series.name}: ${expectedPoint.y}`;
          const actualTooltip = `${actualPoint.series.name}: ${actualPoint.y}`;
          const diffTooltip = `Difference: ${Math.abs(expectedPoint.y - actualPoint.y)}`;
          return `<b>${this.x}</b><br/>${expectedTooltip}<br/>${actualTooltip}<br/>${diffTooltip}`;
        },
        shared: true
      },
      colors: [
        "#004A9C",
        "#50B8FF"
      ],
      series: series,
      credits: {
        enabled: false
      }
    };

    const columns = ["churn_rate", "age"];
    const selectOptions = columns.map(col => ({ value: col, label: col }));

    return (
      <div className="validation-results-overview">
        <div className="overview-summary">
          <div className="overview-summary-center">
            <div className="overview-heading font-bold">Overview</div>
            <div className="overview-contract-container">
              <div className="overview-contract-name">{validationResult.data_contract}</div>
              <div className="i--icon-open" />
            </div>
            <div className="overview-labels font-bold">
              Monitor Name:<br />
              Job ID:<br />
              Time:<br />
              User:<br />
              Row count:
            </div>
            <div className="overview-values">
              {validationResult.monitor_package}<br />
              {validationResult.job_id}<br />
              {date}<br />
              {validationResult.user}<br />
              {rowCount}
            </div>
          </div>
        </div>
        <div className="overview-graph">
          <HighchartsReact highcharts={Highcharts} options={options} />
        </div>
        <div className="overview-graph-stats">
          <Select className="attribute-select" defaultValue={columns[0]} options={selectOptions} />
          <div className="attribute-data-container">
            <div className="attribute-data-label">
              <div className="light-blue-box" />Expected Data
            </div>
            <div className="attribute-data-container-left">
              Percent Missing:<br />Minimum:<br />Maximum:<br />
            </div>
            <div className="attribute-data-container-right">
              10%<br />-1253.45<br />1010002.55<br />
            </div>
          </div>
          <div className="attribute-data-container">
            <div className="attribute-data-label">
              <div className="dark-blue-box" />Actual Data
            </div>
            <div className="attribute-data-container-left">
              Percent Missing:<br />Minimum:<br />Maximum:<br />
            </div>
            <div className="attribute-data-container-right">
              10%<br />-1304.52<br />1221341.50<br />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ValidationResultsOverview.propTypes = {
  validationResult: PropTypes.object
};

ValidationResultsOverview.defaultProps = {
  validationResult: {}
};

export default ValidationResultsOverview;
