import React from 'react';
import Plot from 'react-plotly.js';
import Select from 'react-select';
import PropTypes from 'prop-types';


class ParCoordsGraph extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      jobs: this.props.jobs,
      allParamNames: this.props.allInputParams,
      allMetricNames: this.props.allMetrics,
      selectedParamNames: this.props.allInputParams,
      selectedMetricNames: this.props.allMetrics,
      data: [],
    };

    this.formatJobData = this.formatJobData.bind(this);
    this.onChangeParam = this.onChangeParam.bind(this);
    this.onChangeMetric = this.onChangeMetric.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    const { jobs } = this.state;

    if (jobs !== nextProps.jobs) {
      this.setState({ jobs: nextProps.jobs }, () => {
        this.formatJobData();
      });
    }

    this.setState({
      allParamNames: nextProps.allInputParams.map(p => p.name),
      allMetricNames: nextProps.allMetrics.map(m => m.name),
    });
  }

  formatJobData() {
    const {
      jobs, selectedParamNames, selectedMetricNames, allParamNames, allMetricNames,
    } = this.state;

    const trace = {
      type: 'parcoords',
    };

    const paramTraceDimensions = [];
    let paramNamesToShow = selectedParamNames;
    let metricNamesToShow = selectedMetricNames;

    if (selectedParamNames.length === 0 && selectedMetricNames.length === 0) {
      paramNamesToShow = allParamNames;
      metricNamesToShow = allMetricNames;
    }

    paramNamesToShow.forEach(param => {
      paramTraceDimensions.push({
        label: param,
        values: [],
      });
    });

    const metricTraceDimensions = [];

    metricNamesToShow.forEach(metric => {
      metricTraceDimensions.push({
        label: metric,
        values: [],
      });
    });

    jobs.forEach(job => {
      paramTraceDimensions.forEach(traceDimension => {
        const foundJobParam = job.input_params.filter(jobParam => {
          return jobParam.name === traceDimension.label;
        });

        if (foundJobParam.length === 0) {
          traceDimension.values.push(null);
        } else {
          traceDimension.values.push(foundJobParam[0].value);
        }
      });

      metricTraceDimensions.forEach(traceDimension => {
        const foundJobMetric = job.output_metrics.filter(jobMetric => {
          return jobMetric.name === traceDimension.label;
        });

        if (foundJobMetric.length === 0) {
          traceDimension.values.push(null);
        } else {
          traceDimension.values.push(foundJobMetric[0].value);
        }
      });
    });

    trace.dimensions = [...paramTraceDimensions, ...metricTraceDimensions];
    const data = [trace];
    this.setState({ data: data });
  }

  onChangeParam(selectedOptions) {
    if (selectedOptions && selectedOptions.length > 0) {
      this.setState({ selectedParamNames: selectedOptions.map(m => m.value) }, this.formatJobData);
    } else {
      this.setState({ selectedParamNames: [] }, this.formatJobData);
    }
  }

  onChangeMetric(selectedOptions) {
    if (selectedOptions && selectedOptions.length > 0) {
      this.setState({ selectedMetricNames: selectedOptions.map(m => m.value) }, this.formatJobData);
    } else {
      this.setState({ selectedMetricNames: [] }, this.formatJobData);
    }
  }

  render() {
    const { data, allMetricNames, allParamNames } = this.state;

    const metricOptions = allMetricNames.map(metric => {
      return { value: metric, label: metric };
    });
    const paramOptions = allParamNames.map(param => {
      return { value: param, label: param };
    });

    return (
      <div className="par-coords-graph-container">
        <div className="par-coords-graph-header">
          <h3 className="section-title">Metrics and Parameters</h3>
          <div className="par-coords-graph-select">
            <Select
              onChange={this.onChangeParam}
              options={paramOptions}
              placeholder="Parameters"
              className="react-select"
              isMulti
            />
            <Select
              onChange={this.onChangeMetric}
              options={metricOptions}
              placeholder="Metrics"
              className="react-select"
              isMulti
            />
          </div>
        </div>
        <Plot data={data} layout={{ autosize: true }} useResizeHandler />
      </div>
    );
  }
}

ParCoordsGraph.propTypes = {
  jobs: PropTypes.array,
  allInputParams: PropTypes.array,
  allMetrics: PropTypes.array,
};

ParCoordsGraph.defaultProps = {
  jobs: [],
  allInputParams: [],
  allMetrics: [],
};

export default ParCoordsGraph;
