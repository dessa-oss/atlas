import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import BaseActions from "../../../actions/BaseActions";

const SystemHealth = props => {
  const [showPopulationTab, setShowPopulationTab] = React.useState(true);
  const [showDataQualityTab, setShowDataQualityTab] = React.useState(false);
  const [listFiles, setListFiles] = React.useState([]);
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [data, setData] = React.useState();

  const switchToPopulationShiftTab = () => {
    setShowPopulationTab(true);
    setShowDataQualityTab(false);
  };

  const switchToDataQualityTab = () => {
    setShowPopulationTab(false);
    setShowDataQualityTab(true);
  };

  const loadAnotherFile = fileName => {
    setSelectedFile(fileName);
    BaseActions.getFromApiary("files/health/" + fileName).then(result => {
      if (result) {
        setData(result);
      }
    });
  };

  React.useEffect(() => {
    BaseActions.getFromApiary("files/health").then(result => {
      if (result) {
        setListFiles(result);
        if (selectedFile == null) {
          loadAnotherFile(result[0]);
          document.getElementById("dropdownFiles").selectedIndex = 1;
        }
      }
    });
  }, []);

  const getValidationColor = validation_value => {
    if (validation_value == "critical") {
      return "critical";
    } else if (validation_value == "healthy") {
      return "healthy";
    } else if (validation_value == "warning") {
      return "warning";
    } else {
      return "none";
    }
  };

  const onChangeOption = event => {
    if (event.target.value != "") {
      loadAnotherFile(event.target.value);
    } else {
      setData(null);
    }
  };

  const renderPopulatioShiftTab = () => {
    if (showPopulationTab) {
      if (data == undefined) {
        return (
          <div className="i--image-nothing-here health-state-zero">
            <div class="text-no-reports-loaded">
              You haven't loaded any reports
            </div>
          </div>
        );
      }
      return (
        <div className={`system-health-table table-2`}>
          <table>
            <tr>
              <th>PSI</th>
              <th>Attribute Name</th>
              <th>validation outcome</th>
            </tr>
            {data.population_shift.details_by_attribute.length > 0 &&
              data.population_shift.details_by_attribute.map(row => {
                if (row === "") return;
                return (
                  <tr>
                    <td>{row.PSI}</td>
                    <td>{row.attribute_name}</td>
                    <td className={getValidationColor(row.validation_outcome)}>
                      {row.validation_outcome}
                      <div className="circle" />{" "}
                    </td>
                  </tr>
                );
              })}
          </table>
        </div>
      );
    } else {
      return;
    }
  };

  const renderDataQualityTab = () => {
    if (showDataQualityTab) {
      if (data == undefined) {
        return (
          <div className="i--image-nothing-here">
            <div class="text-no-reports-loaded">
              You haven't loaded any reports
            </div>
          </div>
        );
      }
      return (
        <div className={`system-health-table table-2`}>
          <table>
            <tr>
              <th>% non NUMERIC INFERENCE PERIOD</th>
              <th>% non NUMERIC REFERENCE PERIOD</th>
              <th>% null INFERENCE PERIOD</th>
              <th>% null REFERENCE PERIOD</th>
              <th>% REMAINING INFERENCE PERIOD</th>
              <th>% REMAINING REFERENCE PERIOD</th>
              <th>% zero INFERENCE PERIOD</th>
              <th>% zero REFERENCE PERIOD</th>
              <th>% ATTRIBUTE NAME</th>
              <th>% VALIDATION OUTCOME</th>
            </tr>
            {data.data_quality.details_by_attribute.length > 0 &&
              data.data_quality.details_by_attribute.map(row => {
                if (row === "") return;
                return (
                  <tr>
                    <td>
                      {JSON.stringify(row.pct_non_numeric_inference_period)}
                    </td>
                    <td>{row.pct_non_numeric_reference_period}</td>
                    <td>{row.pct_null_inference_period}</td>
                    <td>{row.pct_null_reference_period}</td>
                    <td>{row.pct_remaining_inference_period}</td>
                    <td>{row.pct_remaining_reference_period}</td>
                    <td>{row.pct_zero_inference_period}</td>
                    <td>{row.pct_zero_reference_period}</td>
                    <td>{row.attribute_name}</td>
                    <td className={getValidationColor(row.validation_outcome)}>
                      {row.validation_outcome}
                      <div className="circle" />
                    </td>
                  </tr>
                );
              })}
          </table>
        </div>
      );
    } else {
      return;
    }
  };
  // data != undefined ?
  let mainWindow = (
    <Layout tab="Health" title="Data Health">
      <div className="new-systemhealth-container-deployment">
        <label className="new-systemhealth-section font-bold">
          DATA HEALTH SUMMARY
        </label>
        <div className="main-display-data-health">
          <div className="left-side">
            <p className="">
              Foundations validates model input data in production automatically
              to catch data abnormalities in real-time. Please select a data
              validation report to review.
            </p>
            <div className="model-performance-filter-container">
              <label>Select report:</label>
              {
                <div className="sh-model-performance-filter">
                  <select
                    id="dropdownFiles"
                    className="manage-interface-modal-select"
                    onChange={onChangeOption}
                  >
                    {listFiles.length > 0 &&
                      listFiles.map(option => {
                        return <option key={option}>{option}</option>;
                      })}
                  </select>
                </div>
              }
            </div>
            <div className="summary-container">
              <p>Inference period:</p>
              <p>
                {data == undefined
                  ? "no report selected"
                  : data.inference_period}
              </p>
              <p>Reference period:</p>
              <p>
                {data == undefined
                  ? "no report selected"
                  : data.reference_period}
              </p>
              <p>Row count difference:</p>
              <p>
                {data == undefined ? "no report selected" : data.row_cnt_diff}
              </p>
              <p>Missing columns:</p>
              <p>
                {data == undefined
                  ? "no report selected"
                  : data.missing_columns}
              </p>
            </div>
          </div>
          <div className="right-side">
            <div
              className={
                showPopulationTab
                  ? "header-population-shift active"
                  : "header-population-shift"
              }
              onClick={switchToPopulationShiftTab}
            >
              <div className="header-title subheader font-bold">
                POPULATION SHIFT
              </div>
              <div className="header-summary">
                <div
                  className={
                    data == undefined ||
                    data.population_shift.summary.warning === 0
                      ? "warning none"
                      : "warning"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.population_shift.summary.warning}
                  <p>Warning</p>
                </div>
                <div
                  className={
                    data == undefined ||
                    data.population_shift.summary.healthy === 0
                      ? "healthy none"
                      : "healthy"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.population_shift.summary.healthy}
                  <p>Healthy</p>
                </div>
                <div
                  className={
                    data == undefined ||
                    data.population_shift.summary.critical === 0
                      ? "critical none"
                      : "critical"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.population_shift.summary.critical}
                  <p>Critical</p>
                </div>
              </div>
            </div>
            <div
              className={
                showDataQualityTab
                  ? "header-data-quality active"
                  : "header-data-quality"
              }
              onClick={switchToDataQualityTab}
            >
              <div className="header-title subheader font-bold">
                DATA QUALITY
              </div>
              <div className="header-summary">
                <div
                  className={
                    data == undefined || data.data_quality.summary.warning === 0
                      ? "warning none"
                      : "warning"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.data_quality.summary.warning}
                  <p>Warning</p>
                </div>
                <div
                  className={
                    data == undefined || data.data_quality.summary.healthy === 0
                      ? "healthy none"
                      : "healthy"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.data_quality.summary.healthy}
                  <p>Healthy</p>
                </div>
                <div
                  className={
                    data == undefined ||
                    data.data_quality.summary.critical === 0
                      ? "critical none"
                      : "critical"
                  }
                >
                  {data == undefined
                    ? "N/A"
                    : data.data_quality.summary.critical}
                  <p>Critical</p>
                </div>
              </div>
            </div>
            <div className="data-display">
              <div
                id="population-shift-table"
                className={
                  showPopulationTab
                    ? "system-health-table-container"
                    : "system-health-table-container hidden"
                }
              >
                {renderPopulatioShiftTab()}
              </div>
              <div
                id="data-quality-table"
                className={
                  showDataQualityTab
                    ? "system-health-table-container"
                    : "system-health-table-container hidden"
                }
              >
                {renderDataQualityTab()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );

  return <div>{mainWindow}</div>;
};

SystemHealth.propTypes = {
  history: PropTypes.object
};

export default withRouter(SystemHealth);
