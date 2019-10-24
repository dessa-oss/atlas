import React, { Component } from "react";
import moment from "moment";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import Select from "react-select";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsOverview extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedAttribute: null,
      selectedOverview: {
        category_names: [],
        expected_data: {
          percentage_missing: null,
          minimum: null,
          maximum: null,
          data: []
        },
        actual_data: {
          percentage_missing: null,
          minimum: null,
          maximum: null,
          data: []
        }
      }
    };

    this.reload = this.reload.bind(this);
    this.onChangeAttribute = this.onChangeAttribute.bind(this);
  }

  componentDidMount() {
    const { validationResult } = this.props;

    validationResult.attribute_names = ["churn_rate", "age"]; // Remove this on update
    if (validationResult.attribute_names.length > 0) {
      this.setState({ selectedAttribute: validationResult.attribute_names[0] }, this.reload);
    } else {
      this.reload();
    }
  }

  async reload() {
    const { selectedAttribute } = this.state;
    const { location, validationResult } = this.props;

    if (location && !CommonActions.isEmptyObject(validationResult) && selectedAttribute) {
      const overview = await ValidationResultsActions.getOverviewForAttribute(
        validationResult,
        location.state.project.name,
        selectedAttribute
      );
      this.setState({ selectedOverview: overview });
    }
  }

  onChangeAttribute(selectedOption) {
    this.setState({ selectedAttribute: selectedOption.value }, this.reload);
  }

  render() {
    const { selectedOverview } = this.state;
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");
    const sign = validationResult.row_count.row_count_diff >= 0 ? "+" : "-";
    const rowDiff = Math.round(Math.abs(validationResult.row_count.row_count_diff) * 1000) / 1000;
    const rowCount = `${validationResult.row_count.expected_row_count} -> ${validationResult.row_count.actual_row_count} (${sign}${rowDiff}%)`; // eslint-disable-line max-len

    const binLabels = selectedOverview.category_names;
    const series = [
      {
        name: "Expected Data",
        data: selectedOverview.expected_data.data
      },
      {
        name: "Actual Data",
        data: selectedOverview.actual_data.data
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

    // const columns = validationResult.attribute_names;
    const columns = ["churn_rate", "age"];
    const selectOptions = columns.map(col => ({ value: col, label: col }));

    const expectedMissing = CommonActions.decimalToPercentage(selectedOverview.expected_data.percentage_missing);
    const expectedMinimum = selectedOverview.expected_data.minimum;
    const expectedMaximum = selectedOverview.expected_data.maximum;
    const actualMissing = CommonActions.decimalToPercentage(selectedOverview.actual_data.percentage_missing);
    const actualMinimum = selectedOverview.actual_data.minimum;
    const actualMaximum = selectedOverview.actual_data.maximum;

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
          <Select
            className="attribute-select"
            defaultValue={selectOptions[0]}
            options={selectOptions}
            onChange={this.onChangeAttribute}
          />
          <div className="attribute-data-container">
            <div className="attribute-data-label">
              <div className="light-blue-box" />Expected Data
            </div>
            <div className="attribute-data-container-left">
              Percent Missing:<br />Minimum:<br />Maximum:<br />
            </div>
            <div className="attribute-data-container-right">
              {expectedMissing}<br />{expectedMinimum}<br />{expectedMaximum}<br />
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
              {actualMissing}<br />{actualMinimum}<br />{actualMaximum}<br />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ValidationResultsOverview.propTypes = {
  location: PropTypes.object,
  validationResult: PropTypes.object
};

ValidationResultsOverview.defaultProps = {
  location: {},
  validationResult: {}
};

export default ValidationResultsOverview;
