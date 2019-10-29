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
      selectedOverview: this.defaultSelectedOverview(),
      isDefaultSelectedOverview: true
    };

    this.reload = this.reload.bind(this);
    this.onChangeAttribute = this.onChangeAttribute.bind(this);
    this.defaultSelectedOverview = this.defaultSelectedOverview.bind(this);
  }

  componentDidMount() {
    const { validationResult } = this.props;

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
      let overview = await ValidationResultsActions.getOverviewForAttribute(
        validationResult,
        location.state.project.name,
        selectedAttribute
      );

      let isDefaultSelectedOverview = false;

      if (overview.expected_data_summary === null || overview.actual_data_summary === null) {
        overview = this.defaultSelectedOverview();
        isDefaultSelectedOverview = true;
      } else {
        overview.actual_data_summary.percentage_missing = CommonActions.decimalToPercentage(
          overview.actual_data_summary.percentage_missing
        );
        overview.expected_data_summary.percentage_missing = CommonActions.decimalToPercentage(
          overview.expected_data_summary.percentage_missing
        );
      }

      this.setState({ selectedOverview: overview, isDefaultSelectedOverview: isDefaultSelectedOverview });
    }
  }

  onChangeAttribute(selectedOption) {
    this.setState({ selectedAttribute: selectedOption.value }, this.reload);
  }

  defaultSelectedOverview() {
    return {
      expected_data_summary: {
        percentage_missing: "N/A",
        minimum: "N/A",
        maximum: "N/A"
      },
      actual_data_summary: {
        percentage_missing: "N/A",
        minimum: "N/A",
        maximum: "N/A"
      },
      binned_data: {
        bins: [],
        data: {
          expected_data: [],
          actual_data: []
        }
      }
    };
  }

  render() {
    const { selectedOverview, isDefaultSelectedOverview } = this.state;
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");
    const sign = validationResult.row_count.row_count_diff >= 0 ? "+" : "-";
    const rowDiff = Math.round(Math.abs(validationResult.row_count.row_count_diff) * 1000) / 1000;
    const rowCount = `${validationResult.row_count.expected_row_count} -> ${validationResult.row_count.actual_row_count} (${sign}${rowDiff}%)`; // eslint-disable-line max-len

    const binLabels = selectedOverview.binned_data.bins;
    const series = [
      {
        name: "Reference Data",
        data: selectedOverview.binned_data.data.expected_data,
        color: "#50B8FF"
      },
      {
        name: "Current Data",
        data: selectedOverview.binned_data.data.actual_data,
        color: "#004A9C"
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
          const diffTooltip = `<b>Difference:</b> ${Math.abs(expectedPoint.y - actualPoint.y)}`;
          return `<b>${this.x}</b><br/>${expectedTooltip}<br/>${actualTooltip}<br/>${diffTooltip}`;
        },
        shared: true
      },
      series: series,
      credits: {
        enabled: false
      }
    };

    const columns = validationResult.attribute_names;
    const selectOptions = columns.map(col => ({ value: col, label: col }));

    const expectedMissing = selectedOverview.expected_data_summary.percentage_missing;
    const expectedMinimum = selectedOverview.expected_data_summary.minimum;
    const expectedMaximum = selectedOverview.expected_data_summary.maximum;
    const actualMissing = selectedOverview.actual_data_summary.percentage_missing;
    const actualMinimum = selectedOverview.actual_data_summary.minimum;
    const actualMaximum = selectedOverview.actual_data_summary.maximum;

    const graph = (
      isDefaultSelectedOverview
        ? (
          <div>
            <div className="empty-overview-graph" />
            This column type is not supported yet.
          </div>
        )
        : <HighchartsReact highcharts={Highcharts} options={options} />
    );

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
          {graph}
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
              <div className="light-blue-box" />Reference Data
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
              <div className="dark-blue-box" />Current Data
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
