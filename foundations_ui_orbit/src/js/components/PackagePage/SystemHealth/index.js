import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import PropTypes from "prop-types";
import ModalTutorial from "../../common/ModalTutorial";
import ValidationResultsTable from "./ValidationResultsTable";
import ValidationResultsDetails from "./ValidationResultsDetails";

class SystemHealth extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedValidationResult: {}
    };

    this.selectRow = this.selectRow.bind(this);
  }

  selectRow(selectedResult) {
    this.setState({ selectedValidationResult: selectedResult });
  }

  // const [showSchemaTab, setShowSchemaTab] = React.useState(true);
  // const [showPopulationTab, setShowPopulationTab] = React.useState(false);
  // const [showDataQualityTab, setShowDataQualityTab] = React.useState(false);
  // const [data, setData] = React.useState();
  // const [options, setOptions] = React.useState([]);
  // const [selectedInferencePeriod, setSelectedInferencePeriod] = React.useState("");
  // const [selectedModelPackage, setSelectedModelPackage] = React.useState("");
  // const [selectedDataContract, setSelectedDataContract] = React.useState("");
  // const [rowCountDifference, setRowCountDifference] = React.useState("No Report Selected");
  // const [tutorialVisible, setTutorialVisible] = React.useState(false);

  // const onToggleTutorial = () => {
  //   let value = !tutorialVisible;
  //   setTutorialVisible(value);
  // };

  // const switchToSchemaTab = () => {
  //   setShowSchemaTab(true);
  //   setShowPopulationTab(false);
  //   setShowDataQualityTab(false);
  // };

  // const switchToPopulationShiftTab = () => {
  //   setShowSchemaTab(false);
  //   setShowPopulationTab(true);
  //   setShowDataQualityTab(false);
  // };

  // const switchToDataQualityTab = () => {
  //   setShowSchemaTab(false);
  //   setShowPopulationTab(false);
  //   setShowDataQualityTab(true);
  // };

  // const formatPercentage = val => {
  //   if (!Number.isNaN(val)) {
  //     let percentage = val * 100;
  //     if (Number.isInteger(percentage)) {
  //       return percentage;
  //     }
  //     return percentage.toFixed(1);
  //   }
  //   return 0;
  // };

  // const reload = () => {
  //   const { location } = props;

  //   get(`projects/${location.state.project.name}/validation_report_list`).then(result => {
  //     if (result) {
  //       let entries = [];
  //       result.forEach(resultItem => {
  //         const value = moment(resultItem.inference_period)
  //           .format("YYYY-MM-DD")
  //           .toString();
  //         const found = entries.find(entry => entry.inference_period === value);

  //         if (!found) {
  //           const entry = {
  //             inference_period: value,
  //             model_packages: []
  //           };
  //           entries.push(entry);
  //         }
  //       });

  //       result.forEach(resultItem => {
  //         entries.forEach(entryItem => {
  //           if (moment(resultItem.inference_period).isSame(entryItem.inference_period, "day")) {
  //             const found = entryItem.model_packages.find(item => item.model_package === resultItem.model_package);

  //             if (!found) {
  //               let newModelPackage = {
  //                 model_package: resultItem.model_package,
  //                 data_contracts: []
  //               };
  //               entryItem.model_packages.push(newModelPackage);
  //             }
  //           }
  //         });
  //       });

  //       result.forEach(resultItem => {
  //         entries.forEach(entry => {
  //           if (moment(resultItem.inference_period).isSame(entry.inference_period, "day")) {
  //             entry.model_packages.forEach(modelPackage => {
  //               if (modelPackage.model_package === resultItem.model_package) {
  //                 let dataContracts = modelPackage.data_contracts;
  //                 const found = dataContracts.find(dataContract => dataContract === resultItem.data_contract);

  //                 if (!found) {
  //                   modelPackage.data_contracts.push(resultItem.data_contract);
  //                 }
  //               }
  //             });
  //           }
  //         });
  //       });

  //       const sortedEntries = entries.sort((a, b) => {
  //         const dateA = new Date(a.inference_period);
  //         const dateB = new Date(b.inference_period);

  //         return dateB - dateA;
  //       });

  //       setOptions(sortedEntries);
  //     }
  //   });
  // };

  // React.useEffect(() => {
  //   reload();
  // }, []);

  // const getValidationColor = validationValue => {
  //   if (validationValue === "critical") {
  //     return "critical";
  //   } if (validationValue === "healthy") {
  //     return "healthy";
  //   } if (validationValue === "warning") {
  //     return "warning";
  //   }
  //   return "none";
  // };

  // /* eslint-disable react/jsx-curly-brace-presence */
  // const renderSchemaTab = () => {
  //   if (showSchemaTab) {
  //     if (data === undefined) {
  //       return (
  //         <div className="i--image-nothing-here health-state-zero">
  //           <div className="text-no-reports-loaded">
  //             You haven&#39;t loaded any reports
  //           </div>
  //         </div>
  //       );
  //     }
  //     return (
  //       <div className="system-health-table table-2">
  //         <table>
  //           <tr>
  //             <th>Attribute Name</th>
  //             <th>Data Type</th>
  //             <th>Issue Type</th>
  //             <th>Validation Outcome</th>
  //           </tr>
  //           {data.schema.details_by_attribute
  //             && data.schema.details_by_attribute.length > 0
  //             && data.schema.details_by_attribute.map(row => {
  //               if (row === "") return;
  //               return (
  //                 <tr key={row.attribute_name}>
  //                   <td>{row.attribute_name}</td>
  //                   <td>{row.data_type}</td>
  //                   <td>{row.issue_type || ""}</td>
  //                   <td className={getValidationColor(row.validation_outcome)}>
  //                     {row.validation_outcome}
  //                     <div className="circle" />{" "}
  //                   </td>
  //                 </tr>
  //               );
  //             })}
  //         </table>
  //       </div>
  //     );
  //   }
  // };

  // const renderPopulatioShiftTab = () => {
  //   if (showPopulationTab) {
  //     if (data === undefined) {
  //       return (
  //         <div className="i--image-nothing-here health-state-zero">
  //           <div className="text-no-reports-loaded">
  //             You haven&#39;t loaded any reports
  //           </div>
  //         </div>
  //       );
  //     }

  //     return (
  //       <div className="system-health-table table-2">
  //         <table>
  //           <tr>
  //             <th>Attribute Name</th>
  //             <th>Distribution Shift</th>
  //             <th>Validation Outcome</th>
  //           </tr>
  //           {data.population_shift.details_by_attribute
  //             && data.population_shift.details_by_attribute.length > 0
  //             && data.population_shift.details_by_attribute.map(row => {
  //               if (row === "") return;
  //               const isLInfinity = "L-infinity" in row;
  //               const shiftMetric = isLInfinity ? row["L-infinity"] : row.PSI;
  //               return (
  //                 <tr key={row.attribute_name}>
  //                   <td>{row.attribute_name}</td>
  //                   <td>{shiftMetric}</td>
  //                   <td className={getValidationColor(row.validation_outcome)}>
  //                     {row.validation_outcome}
  //                     <div className="circle" />{" "}
  //                   </td>
  //                 </tr>
  //               );
  //             })}
  //         </table>
  //       </div>
  //     );
  //   }
  // };

  // const renderDataQualityTab = () => {
  //   if (showDataQualityTab) {
  //     if (data === undefined) {
  //       return (
  //         <div className="i--image-nothing-here health-state-zero">
  //           <div className="text-no-reports-loaded">
  //             You haven&#39;t loaded any reports
  //           </div>
  //         </div>
  //       );
  //     }
  //     return (
  //       <div className="system-health-table table-2">
  //         <table>
  //           <tr>
  //             <th>Attribute Name</th>
  //             <th>Value</th>
  //             <th>Expected (%)</th>
  //             <th>Actual (%)</th>
  //             <th>Difference</th>
  //             <th>Validation Outcome</th>
  //           </tr>
  //           {data.data_quality.details_by_attribute
  //             && data.data_quality.details_by_attribute.length > 0
  //             && data.data_quality.details_by_attribute.map(row => {
  //               if (row === "") return;
  //               return (
  //                 <tr key={row.attribute_name}>
  //                   <td>{row.attribute_name}</td>
  //                   <td>{row.value}</td>
  //                   <td>{formatPercentage(row.pct_in_reference_data)}</td>
  //                   <td>{formatPercentage(row.pct_in_current_data)}</td>
  //                   <td>{formatPercentage(row.difference_in_pct)}</td>
  //                   <td className={getValidationColor(row.validation_outcome)}>
  //                     {row.validation_outcome}
  //                     <div className="circle" />
  //                   </td>
  //                 </tr>
  //               );
  //             })}
  //         </table>
  //       </div>
  //     );
  //   }
  // };
  // /* eslint-enable react/jsx-curly-brace-presence */

  // const onClickInferencePeriod = value => {
  //   if (value === selectedInferencePeriod) {
  //     setSelectedInferencePeriod("");
  //     setSelectedModelPackage("");
  //     setRowCountDifference("");
  //   } else {
  //     setSelectedInferencePeriod(value);
  //   }
  // };

  // const onClickModelPackage = value => {
  //   if (value === selectedModelPackage) {
  //     setSelectedModelPackage("");
  //   } else {
  //     setSelectedModelPackage(value);
  //   }
  // };

  // const onClickDataContract = value => {
  //   setSelectedDataContract(value);

  //   const { location } = props;

  //   const body = {
  //     inference_period: selectedInferencePeriod,
  //     monitor_package: selectedModelPackage,
  //     data_contract: value
  //   };

  //   post(`projects/${location.state.project.name}/validation_results`, body).then(result => {
  //     if (result) {
  //       setData(result);
  //     }
  //   });
  // };

  // const renderDataContracts = item => {
  //   return item.data_contracts.map(contract => {
  //     return (
  //       <div
  //         className={contract === selectedDataContract
  //           ? "container-health-data-contract selected"
  //           : "container-health-data-contract"}
  //         key={contract}
  //       >
  //         <div
  //           className={contract === selectedDataContract ? "label-data-contract selected" : "label-data-contract"}
  //           onClick={() => onClickDataContract(contract)}
  //         >
  //           {contract}
  //         </div>
  //       </div>
  //     );
  //   });
  // };

  // const renderModelPackages = option => {
  //   return option.model_packages.map(item => {
  //     return (
  //       <div
  //         className="container-health-model-package"
  //         key={item.model_package}
  //       >
  //         <div
  //           className="label-model-package"
  //           onClick={() => onClickModelPackage(item.model_package)}
  //         >
  //           {item.model_package === selectedModelPackage
  //             ? `- ${item.model_package}`
  //             : `+ ${item.model_package}`}
  //         </div>
  //         {item.model_package === selectedModelPackage && renderDataContracts(item)}
  //       </div>
  //     );
  //   });
  // };

  // const renderOptions = () => {
  //   return options.map(option => {
  //     return (
  //       <div
  //         className="container-health-options"
  //         key={option.inference_period}
  //       >
  //         <div
  //           className="label-option"
  //           onClick={() => onClickInferencePeriod(option.inference_period)}
  //         >
  //           {option.inference_period === selectedInferencePeriod
  //             ? `- ${option.inference_period}`
  //             : `+ ${option.inference_period}`}
  //         </div>
  //         {option.inference_period === selectedInferencePeriod && renderModelPackages(option)}
  //       </div>
  //     );
  //   });
  // };

  // const onClickRefreshList = () => {
  //   reload();
  // };

  // data != undefined ?
  render() {
    const { selectedValidationResult } = this.state;

    const location = this.props.location;

    return (
      // <Layout tab="Health" title="Data Health" openTutorial={onToggleTutorial}>
      <Layout tab="Health" title="Data Health">
        <div className="new-systemhealth-container-deployment">
          <div className="main-display-data-health">
            <label className="new-systemhealth-section font-bold">
              Data Validation Results
            </label>
            <div className="systemhealth-body">
              <div className="left-side">
                {/* <div className="i--icon-refresh" onClick={onClickRefreshList} /> */}
                <div className="i--icon-refresh" />
                <div className="validation-results-table-row-header">
                  <div className="val-time-table-cell">Date</div>
                  <div className="val-monitor-table-cell">Monitor Name</div>
                  <div className="val-contract-table-cell">Contract Name</div>
                  <div className="val-critical-table-cell" />
                </div>
                <ValidationResultsTable
                  location={location}
                  onClickRow={this.selectRow}
                  selectedRow={selectedValidationResult}
                />
              </div>
              <div className="right-side">
                <ValidationResultsDetails location={location} selectedValidationResult={selectedValidationResult} />
              </div>
            </div>
          </div>
          {/* <ModalTutorial
            tutorialVisible={tutorialVisible}
            onToggleTutorial={onToggleTutorial}
          /> */}
        </div>
      </Layout>
    );
  }
}

SystemHealth.propTypes = {
  location: PropTypes.object
};

SystemHealth.defaultProps = {
  location: { state: {} }
};

export default withRouter(SystemHealth);
