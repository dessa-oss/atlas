import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import HighchartsReact from "highcharts-react-official";
import Highcharts from "highcharts";

const ModelEvaluation = props => {
  const [open, setOpen] = React.useState(false);

  const onClickOpenChart = () => {
    setOpen(true);
  };

  const onClickCloseChart = () => {
    setOpen(false);
  };

  function getPreviewyAxisData(data) {
    const previewData = data;
    previewData.title.text = null;
    return previewData;
  }

  const { evaluation } = props;

  const options = {
    chart: {},
    title: {
      style: {
        color: "#004A9C",
        fontSize: 14
      },
      text: evaluation.title.text,
      align: "left"
    },
    subtitle: {
      style: {
        color: "#9c9c9c"
      },
      text: `<span class="highcharts-sub">${
        evaluation.series.length
      }</span> predictors`,
      useHTML: true,
      align: "left"
    },
    legend: {
      // layout: "vertical",
      // align: "left",
      // verticalAlign: "middle",
      // itemMarginTop: 10,
      // itemMarginBottom: 10
      enabled: false
    },
    credits: {
      enabled: false
    },
    xAxis: evaluation.xAxis,
    yAxis: getPreviewyAxisData(evaluation.yAxis),
    series: evaluation.series
  };

  const optionsModal = {
    chart: {
      width: 1500
    },
    title: {
      text: evaluation.title.text
    },
    legend: {
      layout: "vertical",
      align: "left",
      verticalAlign: "middle",
      itemMarginTop: 10,
      itemMarginBottom: 10
    },
    credits: {
      enabled: false
    },
    xAxis: options.xAxis,
    yAxis: evaluation.yAxis,
    series: evaluation.series
  };

  return (
    <div className="container-preview">
      <p className="view-report" onClick={onClickOpenChart} />
      <div className="container-chart">
        <HighchartsReact highcharts={Highcharts} options={options} />
      </div>
      <Modal
        isOpen={open}
        toggle={onClickCloseChart}
        className="modal-evaluation-chart"
      >
        <ModalBody>
          <div>
            <HighchartsReact highcharts={Highcharts} options={optionsModal} />
          </div>
        </ModalBody>
      </Modal>
    </div>
  );
};

ModelEvaluation.propTypes = {
  evaluation: PropTypes.object
};

ModelEvaluation.defaultProps = {
  evaluation: {}
};

export default withRouter(ModelEvaluation);
