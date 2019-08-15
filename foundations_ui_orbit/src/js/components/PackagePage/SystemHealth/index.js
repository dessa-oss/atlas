import React from "react";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import { getFromApiary } from "../../../actions/BaseActions";
import PropTypes from "prop-types";
import moment from "moment";

const SystemHealth = props => {
  const [showSchemaTab, setShowSchemaTab] = React.useState(true);
  const [showPopulationTab, setShowPopulationTab] = React.useState(false);
  const [showDataQualityTab, setShowDataQualityTab] = React.useState(false);
  const [data, setData] = React.useState();
  const [options, setOptions] = React.useState([]);
  const [selectedInferencePeriod, setSelectedInferencePeriod] = React.useState("");
  const [selectedModelPackage, setSelectedModelPackage] = React.useState("");
  const [selectedDataContract, setSelectedDataContract] = React.useState("");
  const [rowCountDifference, setRowCountDifference] = React.useState("No Report Selected");

  const switchToSchemaTab = () => {
    setShowSchemaTab(true);
    setShowPopulationTab(false);
    setShowDataQualityTab(false);
  };

  const switchToPopulationShiftTab = () => {
    setShowSchemaTab(false);
    setShowPopulationTab(true);
    setShowDataQualityTab(false);
  };

  const switchToDataQualityTab = () => {
    setShowSchemaTab(false);
    setShowPopulationTab(false);
    setShowDataQualityTab(true);
  };

  const reload = () => {
    const { location } = props;

    getFromApiary(`projects/${location.state.project.name}/validation_report_list`).then(result => {
      if (result) {
        let entries = [];
        result.forEach(resultItem => {
          const value = moment(resultItem.inference_period)
            .format("YYYY-MM-DD")
            .toString();
          const found = entries.find(entry => entry.inference_period === value);

          if (!found) {
            const entry = {
              inference_period: value,
              model_packages: []
            };
            entries.push(entry);
          }
        });

        result.forEach(resultItem => {
          entries.forEach(entryItem => {
            if (resultItem.inference_period === entryItem.inference_period) {
              const found = entryItem.model_packages.find(item => item.model_package === resultItem.model_package);

              if (!found) {
                let newModelPackage = {
                  model_package: resultItem.model_package,
                  data_contracts: []
                };
                entryItem.model_packages.push(newModelPackage);
              }
            }
          });
        });

        result.forEach(resultItem => {
          entries.forEach(entry => {
            if (entry.inference_period === resultItem.inference_period) {
              entry.model_packages.forEach(modelPackage => {
                if (modelPackage.model_package === resultItem.model_package) {
                  let dataContracts = modelPackage.data_contracts;
                  const found = dataContracts.find(dataContract => dataContract === resultItem.data_contract);

                  if (!found) {
                    modelPackage.data_contracts.push(resultItem.data_contract);
                  }
                }
              });
            }
          });
        });

        const sortedEntries = entries.sort((a, b) => {
          const dateA = new Date(a.inference_period);
          const dateB = new Date(b.inference_period);

          return dateA - dateB;
        });

        setOptions(sortedEntries);
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const getValidationColor = validationValue => {
    if (validationValue === "critical") {
      return "critical";
    } if (validationValue === "healthy") {
      return "healthy";
    } if (validationValue === "warning") {
      return "warning";
    }
    return "none";
  };

  const renderSchemaTab = () => {
    if (showSchemaTab) {
      if (data === undefined) {
        return (
          <div className="i--image-nothing-here health-state-zero">
            <div className="text-no-reports-loaded">
              You haven{"'"}t loaded any reports
            </div>
          </div>
        );
      }
      return (
        <div className="system-health-table table-2">
          <table>
            <tr>
              <th>ATTRIBUTE NAME</th>
              <th>DATA TYPE</th>
              <th>ISSUE TYPE</th>
              <th>VALIDATION OUTCOME</th>
            </tr>
            {data.schema.details_by_attribute.length > 0
              && data.schema.details_by_attribute.map(row => {
                console.log("ROW: ", row);
                if (row === "") return;
                return (
                  <tr key={row.attribute_name}>
                    <td>{row.attribute_name}</td>
                    <td>{row.data_type}</td>
                    <td>{row.issue_type || ""}</td>
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
    }
  };

  const renderPopulatioShiftTab = () => {
    if (showPopulationTab) {
      if (data === undefined) {
        return (
          <div className="i--image-nothing-here health-state-zero">
            <div className="text-no-reports-loaded">
              You haven{"'"}t loaded any reports
            </div>
          </div>
        );
      }
      return (
        <div className="system-health-table table-2">
          <table>
            <tr>
              <th>ATTRIBUTE NAME</th>
              <th>POPULATION SHIFT INDEX</th>
              <th>VALIDATION OUTCOME</th>
            </tr>
            {data.population_shift.details_by_attribute.length > 0
              && data.population_shift.details_by_attribute.map(row => {
                if (row === "") return;
                return (
                  <tr key={row.attribute_name}>
                    <td>{row.attribute_name}</td>
                    <td>{row.PSI}</td>
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
    }
  };

  const renderDataQualityTab = () => {
    if (showDataQualityTab) {
      if (data === undefined) {
        return (
          <div className="i--image-nothing-here health-state-zero">
            <div className="text-no-reports-loaded">
              You haven{"'"}t loaded any reports
            </div>
          </div>
        );
      }
      return (
        <div className="system-health-table table-2">
          <table>
            <tr>
              <th>ATTRIBUTE NAME</th>
              <th>VALUE</th>
              <th>% IN REFERENCE DATA</th>
              <th>% IN PRODUCTION DATA</th>
              <th>DIFFERENCE</th>
              <th>VALIDATION OUTCOME</th>
            </tr>
            {data.data_quality.details_by_attribute.length > 0
              && data.data_quality.details_by_attribute.map(row => {
                if (row === "") return;
                return (
                  <tr key={row.attribute_name}>
                    <td>{row.attribute_name}</td>
                    <td>{row.value}</td>
                    <td>{row.pct_in_reference_data}</td>
                    <td>{row.pct_in_inference_data}</td>
                    <td>{row.difference_in_pct}</td>
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
    }
  };

  const onClickInferencePeriod = value => {
    if (value === selectedInferencePeriod) {
      setSelectedInferencePeriod("");
      setSelectedModelPackage("");
      setRowCountDifference("");
    } else {
      setSelectedInferencePeriod(value);
    }
  };

  const onClickModelPackage = value => {
    if (value === selectedModelPackage) {
      setSelectedModelPackage("");
    } else {
      setSelectedModelPackage(value);
    }
  };

  const onClickDataContract = value => {
    setSelectedDataContract(value);

    const { location } = props;

    getFromApiary(`projects/${location.state.project.name}/validation_results`).then(result => {
      if (result) {
        setData(result);
      }
    });
  };

  const renderDataContracts = item => {
    return item.data_contracts.map(contract => {
      return (
        <div
          className={contract === selectedDataContract
            ? "container-health-data-contract selected"
            : "container-health-data-contract"}
          key={contract}
        >
          <div
            className={contract === selectedDataContract ? "label-data-contract selected" : "label-data-contract"}
            onClick={() => onClickDataContract(contract)}
          >
            {contract}
          </div>
        </div>
      );
    });
  };

  const renderModelPackages = option => {
    return option.model_packages.map(item => {
      return (
        <div
          className="container-health-model-package"
          key={item.model_package}
        >
          <div
            className="label-model-package"
            onClick={() => onClickModelPackage(item.model_package)}
          >
            {item.model_package === selectedModelPackage
              ? `- ${item.model_package}`
              : `+ ${item.model_package}`}
          </div>
          {item.model_package === selectedModelPackage && renderDataContracts(item)}
        </div>
      );
    });
  };

  const renderOptions = () => {
    return options.map(option => {
      return (
        <div
          className="container-health-options"
          key={option.inference_period}
        >
          <div
            className="label-option"
            onClick={() => onClickInferencePeriod(option.inference_period)}
          >
            {option.inference_period === selectedInferencePeriod
              ? `- ${option.inference_period}`
              : `+ ${option.inference_period}`}
          </div>
          {option.inference_period === selectedInferencePeriod && renderModelPackages(option)}
        </div>
      );
    });
  };

  // data != undefined ?
  const mainWindow = (
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
            <p className="label-select-reports">Select report:</p>
            <div className="container-health-reports">
              {renderOptions()}
            </div>
            <div className="summary-container">
              <p>Inference period:</p>
              <p>{data !== undefined ? data.inference_period : "No Report Selected"}
              </p>
              <p>Model Package:</p>
              <p>{data !== undefined ? data.model_package : "No Report Selected"}</p>
              <p>Data Contract:</p>
              <p>{data !== undefined ? data.data_contract : "No Report Selected"}</p>
              <p>Row count difference:</p>
              <p>
                {data !== undefined ? data.row_cnt_diff : "No Report Selected"}
              </p>
            </div>
          </div>
          <div className="right-side">
            <div
              className={
                showSchemaTab
                  ? "header-population-shift active"
                  : "header-population-shift"
              }
              onClick={switchToSchemaTab}
            >
              <div className="header-title subheader font-bold">
                SCHEMA CHECK
              </div>
              <div className="header-summary">
                <div
                  className={
                    data === undefined
                      || data.schema.summary.warning === 0
                      ? "warning none"
                      : "warning"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.schema.summary.warning}
                  <p>Warning</p>
                </div>
                <div
                  className={
                    data === undefined
                      || data.schema.summary.healthy === 0
                      ? "healthy none"
                      : "healthy"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.schema.summary.healthy}
                  <p>Healthy</p>
                </div>
                <div
                  className={
                    data === undefined
                      || data.schema.summary.critical === 0
                      ? "critical none"
                      : "critical"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.schema.summary.critical}
                  <p>Critical</p>
                </div>
              </div>
            </div>
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
                    data === undefined
                      || data.population_shift.summary.warning === 0
                      ? "warning none"
                      : "warning"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.population_shift.summary.warning}
                  <p>Warning</p>
                </div>
                <div
                  className={
                    data === undefined
                      || data.population_shift.summary.healthy === 0
                      ? "healthy none"
                      : "healthy"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.population_shift.summary.healthy}
                  <p>Healthy</p>
                </div>
                <div
                  className={
                    data === undefined
                      || data.population_shift.summary.critical === 0
                      ? "critical none"
                      : "critical"
                  }
                >
                  {data === undefined
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
                DATA ABNORMALITY
              </div>
              <div className="header-summary">
                <div
                  className={
                    data === undefined || data.data_quality.summary.warning === 0
                      ? "warning none"
                      : "warning"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.data_quality.summary.warning}
                  <p>Warning</p>
                </div>
                <div
                  className={
                    data === undefined || data.data_quality.summary.healthy === 0
                      ? "healthy none"
                      : "healthy"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.data_quality.summary.healthy}
                  <p>Healthy</p>
                </div>
                <div
                  className={
                    data === undefined
                      || data.data_quality.summary.critical === 0
                      ? "critical none"
                      : "critical"
                  }
                >
                  {data === undefined
                    ? "N/A"
                    : data.data_quality.summary.critical}
                  <p>Critical</p>
                </div>
              </div>
            </div>
            <div className="data-display">
              <div
                id="schema-table"
                className={
                  showSchemaTab
                    ? "system-health-table-container"
                    : "system-health-table-container hidden"
                }
              >
                {renderSchemaTab()}
              </div>
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
  location: PropTypes.object
};

SystemHealth.defaultProps = {
  location: { state: {} }
};

export default withRouter(SystemHealth);
