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
    var previewData = data;
    previewData.title.text = null;
    return previewData;
  }

  function getPreviewxAxisData(data) {
    var month_names_short = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ];
    var previewData = JSON.parse(JSON.stringify(data));
    //previewData.categories.forEach(x => getMonthFromData(x));
    var previewCategories = Array();

    for (var categorie of previewData.categories) {
      var date = new Date(categorie);
      previewCategories.push(month_names_short[date.getMonth()]);
    }

    previewData.categories = previewCategories;

    return previewData;
  }

  const options = {
    chart: {},
    title: {
      style: {
        color: "#004A9C",
        fontSize: 14
      },
      text: props.evaluation.title.text,
      align: "left"
    },
    subtitle: {
      style: {
        color: "#9c9c9c"
      },
      text: `<span class="highcharts-sub">${
        props.evaluation.series.length
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
    xAxis: props.evaluation.xAxis,
    yAxis: getPreviewyAxisData(props.evaluation.yAxis),
    yAxis: {
      labels: {
        enabled: false
      },
      title: false
    },
    series: props.evaluation.series
  };

  const optionsModal = {
    chart: {
      width: 1500
    },
    title: {
      text: props.evaluation.title.text
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
    yAxis: props.evaluation.yAxis,
    series: props.evaluation.series
  };

  return (
    <div className="container-preview">
      <p class="view-report" onClick={onClickOpenChart} />
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
