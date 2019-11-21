import React, {
  Component,
  useState,
  useEffect,
  useRef
} from "react";
import moment from "moment";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import Select from "react-select";
import PropTypes from "prop-types";
import CommonActions from "../../../actions/CommonActions";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";
import OverflowTooltip from "../../common/OverflowTooltip";

const ValidationResultsOverviewGraph = ({
  selectedOverview,
  isDefaultSelectedOverview
}) => {
  const graphDiv = useRef(null);
  const [graphWidth, setGraphWidth] = useState(null);
  const [graphHeight, setGraphHeight] = useState(null);
  const [dataIsNormalized, setDataIsNormalized] = useState(false);

  useEffect(() => {
    if (graphDiv) {
      setGraphWidth(graphDiv.current.clientWidth);
      setGraphHeight(graphDiv.current.clientHeight);
    }
  }, [graphDiv]);

  const toggleDataNormalization = () => {
    setDataIsNormalized(!dataIsNormalized);
  };

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
      type: "column",
      width: graphWidth - 60,
      height: graphHeight - 30
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
      formatter: function formatter() {
        const expectedPoint = this.points[0]; // eslint-disable-line react/no-this-in-sfc
        const actualPoint = this.points[1]; // eslint-disable-line react/no-this-in-sfc
        const expectedTooltip = `${expectedPoint.series.name}: ${expectedPoint.y}`;
        const actualTooltip = `${actualPoint.series.name}: ${actualPoint.y}`;
        const diffTooltip = `<b>Difference:</b> ${Math.abs(
          expectedPoint.y - actualPoint.y
        )}`;
        // eslint-disable-next-line react/no-this-in-sfc
        return `<b>${this.x}</b><br/>${expectedTooltip}<br/>${actualTooltip}<br/>${diffTooltip}`;
      },
      shared: true
    },
    series: series,
    credits: {
      enabled: false
    }
  };

  const graph = isDefaultSelectedOverview ? (
    <div className="empty-overview-graph-container">
      <div className="empty-overview-graph" />
    </div>
  ) : (
    <HighchartsReact highcharts={Highcharts} options={options} />
  );

  return (
    <div className="overview-graph" ref={graphDiv}>
      <div onClick={toggleDataNormalization}>Normalize</div>
      {graph}
    </div>
  );
};

class ValidationResultsOverview extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedAttribute: null,
      selectedOverview: this.defaultSelectedOverview(),
      isDefaultSelectedOverview: true
    };

    this.update = this.update.bind(this);
    this.reload = this.reload.bind(this);
    this.onChangeAttribute = this.onChangeAttribute.bind(this);
    this.defaultSelectedOverview = this.defaultSelectedOverview.bind(this);
    this.onClickOpenInfo = this.onClickOpenInfo.bind(this);
  }

  update() {
    const { validationResult } = this.props;

    if (validationResult.attribute_names.length > 0) {
      this.setState({ selectedAttribute: null }, this.reload);
    } else {
      this.reload();
    }
  }

  componentDidMount() {
    this.update();
  }

  onClickOpenInfo() {
    const { toggleInfo, uuid } = this.props;
    toggleInfo(uuid);
  }

  componentDidUpdate(prevProps) {
    const { validationResult } = this.props;
    if (
      !CommonActions.deepEqual(validationResult, prevProps.validationResult)
    ) {
      this.update();
    }
  }

  async reload() {
    const { selectedAttribute } = this.state;
    const { location, validationResult } = this.props;

    if (location && !CommonActions.isEmptyObject(validationResult)) {
      if (selectedAttribute) {
        let overview = await ValidationResultsActions.getOverviewForAttribute(
          validationResult,
          location.state.project.name,
          selectedAttribute.value
        );

        let isDefaultSelectedOverview = false;

        if (
          overview.expected_data_summary === null
          || overview.actual_data_summary === null
        ) {
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

        this.setState({
          selectedOverview: overview,
          isDefaultSelectedOverview: isDefaultSelectedOverview
        });
      } else {
        this.setState({
          selectedOverview: this.defaultSelectedOverview(),
          isDefaultSelectedOverview: true
        });
      }
    }
  }

  onChangeAttribute(selectedOption) {
    this.setState({ selectedAttribute: selectedOption }, this.reload);
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
    const {
      selectedAttribute,
      selectedOverview,
      isDefaultSelectedOverview
    } = this.state;
    const { validationResult } = this.props;
    const date = moment(validationResult.date).format("YYYY-MM-DD h:mm A");
    const sign = validationResult.row_count.row_count_diff >= 0 ? "+" : "-";
    const rowDiff = CommonActions.decimalToPercentage(
      validationResult.row_count.row_count_diff
    );
    const rowCount = `${validationResult.row_count.expected_row_count} -> ${validationResult.row_count.actual_row_count} (${sign}${rowDiff})`; // eslint-disable-line max-len

    const columns = validationResult.attribute_names;
    const selectOptions = columns.map(col => ({ value: col, label: col }));

    const expectedMissing = CommonActions.nullToNA(
      selectedOverview.expected_data_summary.percentage_missing
    );
    const expectedMinimum = CommonActions.nullToNA(
      selectedOverview.expected_data_summary.minimum
    );
    const expectedMaximum = CommonActions.nullToNA(
      selectedOverview.expected_data_summary.maximum
    );
    const actualMissing = CommonActions.nullToNA(
      selectedOverview.actual_data_summary.percentage_missing
    );
    const actualMinimum = CommonActions.nullToNA(
      selectedOverview.actual_data_summary.minimum
    );
    const actualMaximum = CommonActions.nullToNA(
      selectedOverview.actual_data_summary.maximum
    );

    const graph = (
      <ValidationResultsOverviewGraph
        selectedOverview={selectedOverview}
        isDefaultSelectedOverview={isDefaultSelectedOverview}
      />
    );

    return (
      <div className="validation-results-overview">
        <div className="overview-summary">
          <div className="overview-summary-center">
            <div className="overview-heading font-bold">Overview</div>
            <div className="overview-contract-container">
              <div className="overview-contract-name">
                {validationResult.data_contract}
              </div>
              <div className="i--icon-open" onClick={this.onClickOpenInfo} />
            </div>
            <div className="overview-labels-values-container">
              <div className="overview-labels font-bold">
                Monitor Name:
                <br />
                Job ID:
                <br />
                Time:
                <br />
                User:
                <br />
                Row count:
              </div>
              <div className="overview-values">
                <OverflowTooltip text={validationResult.monitor_package} />
                <br />
                <OverflowTooltip text={validationResult.job_id} />
                <br />
                <OverflowTooltip text={date} />
                <br />
                <OverflowTooltip text={validationResult.user} />
                <br />
                <OverflowTooltip text={rowCount} />
                <br />
              </div>
            </div>
          </div>
        </div>
        {graph}
        <div className="overview-graph-stats">
          <div className="overview-graph-stats-center">
            <Select
              className="attribute-select"
              defaultValue={null}
              value={selectedAttribute}
              options={selectOptions}
              onChange={this.onChangeAttribute}
            />
            <div className="attribute-data-container">
              <div className="attribute-data-label">
                <div className="light-blue-box" />
                Reference Data
              </div>
              <div className="attribute-data-container-left-right-container">
                <div className="attribute-data-container-left">
                  Percent Missing:
                  <br />
                  Minimum:
                  <br />
                  Maximum:
                  <br />
                </div>
                <div className="attribute-data-container-right">
                  <OverflowTooltip text={expectedMissing} />
                  <br />
                  <OverflowTooltip text={expectedMinimum} />
                  <br />
                  <OverflowTooltip text={expectedMaximum} />
                  <br />
                </div>
              </div>
            </div>
            <div className="attribute-data-container">
              <div className="attribute-data-label">
                <div className="dark-blue-box" />
                Current Data
              </div>
              <div className="attribute-data-container-left-right-container">
                <div className="attribute-data-container-left">
                  Percent Missing:
                  <br />
                  Minimum:
                  <br />
                  Maximum:
                  <br />
                </div>
                <div className="attribute-data-container-right">
                  <OverflowTooltip text={actualMissing} />
                  <br />
                  <OverflowTooltip text={actualMinimum} />
                  <br />
                  <OverflowTooltip text={actualMaximum} />
                  <br />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ValidationResultsOverviewGraph.propTypes = {
  selectedOverview: PropTypes.object,
  isDefaultSelectedOverview: PropTypes.bool
};

ValidationResultsOverviewGraph.defaultProps = {
  selectedOverview: {},
  isDefaultSelectedOverview: true
};

ValidationResultsOverview.propTypes = {
  location: PropTypes.object,
  validationResult: PropTypes.object,
  toggleInfo: PropTypes.func,
  uuid: PropTypes.string
};

ValidationResultsOverview.defaultProps = {
  location: {},
  validationResult: {},
  toggleInfo: () => {},
  uuid: ""
};

export default ValidationResultsOverview;
