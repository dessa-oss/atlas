import React from "react";
import { withRouter } from "react-router-dom";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { get } from "../../../actions/BaseActions";

const PredictorChart = () => {
  const [categories, setCategories] = React.useState([]);
  const [xAxeTitles, setxAxeTitles] = React.useState([]);

  function getAxesValuesAndData(data) {
    let keyNames = Object.keys(data[0]);
    keyNames = keyNames.slice(1);
    setxAxeTitles(keyNames);
    const categoriesArray = [];
    data.forEach(oneLine => {
      const arrayOfValues = [];
      keyNames.forEach(key => {
        arrayOfValues.push(parseInt(oneLine[key], 10));
      });
      const serie = {
        name: oneLine.name,
        data: arrayOfValues
      };
      categoriesArray.push(serie);
    });
    setCategories(categoriesArray);
  }

  React.useEffect(() => {
    get("populations/size").then(result => {
      if (result) {
        getAxesValuesAndData(result.data);
      }
    });
  }, []);

  const options = {
    chart: {
      type: "column",
      width: 800
    },
    title: {
      text: "POPULATION SIZE OVER TIME"
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
    xAxis: {
      categories: xAxeTitles
    },
    yAxis: {
      min: 0,
      lineWidth: 1,
      title: {
        text: null
      }
    },
    tooltip: {
      pointFormat:
        '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
      shared: true
    },
    plotOptions: {
      column: {
        stacking: "percentage"
      },
      series: {
        pointWidth: 40
      }
    },
    colors: [
      "#E9F3FF",
      "#4A9CF8",
      "#004A9C",
      "#668F69",
      "#EA7317",
      "#533A71",
      "#2176AE",
      "#B66D0D",
      "#FBB13C"
    ],
    series: categories
  };

  return (
    <div>
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  );
};

PredictorChart.propTypes = {};

PredictorChart.defaultProps = {};

export default withRouter(PredictorChart);
