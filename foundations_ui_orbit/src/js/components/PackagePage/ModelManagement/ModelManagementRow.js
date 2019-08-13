import React, { Component } from "react";
import PropTypes from "prop-types";
import ModelManagementDetail from "./ModelManagementDetails";
import ModelRecalibrationModal from "./ModelRecalibrationModal";
import BaseActions from "../../../actions/BaseActions";
import NewModelRecalibrationModal from "./NewModelRecalibrationModal";

class ModelManagementRow extends Component {
  constructor(props) {
    super(props);
    this.clickDetails = this.clickDetails.bind(this);
    this.clickPromoteRetire = this.clickPromoteRetire.bind(this);
    this.clickRecalibrate = this.clickRecalibrate.bind(this);
    this.onChangeDefault = this.onChangeDefault.bind(this);
    this.clickRetire = this.clickRetire.bind(this);
    this.clickActivate = this.clickActivate.bind(this);
    this.state = {
      rowData: this.props.rowData,
      isDetail: this.props.isDetail,
      toggleDetailRow: this.props.toggleDetailRow,
      rowNum: this.props.rowNum,
      isRecalibrate: false
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ isDetail: nextProps.isDetail });
  }

  clickDetails() {
    const { toggleDetailRow, rowNum, isDetail } = this.state;
    if (isDetail) {
      toggleDetailRow(-1);
    } else {
      toggleDetailRow(rowNum);
    }
  }

  clickPromoteRetire() {
    const { rowData } = this.state;
    const newPromoteRetire =
      rowData.status === "Active" ? "Inactive" : "Active";
    const finalData =
      '{"PackageName": "' +
      rowData.model_package_name +
      '", "PromoteRetire": "' +
      newPromoteRetire +
      '"}';

    BaseActions.postJSONFile(
      "files/promoteRetire",
      "model_list.json",
      finalData
    );
  }

  clickRecalibrate() {
    const { isRecalibrate } = this.state;
    this.setState({ isRecalibrate: !isRecalibrate });
  }

  onChangeDefault(e) {
    if (this.state.rowData.default === false) {
      let body = {
        default_model: this.state.rowData.model_name
      };

      BaseActions.putApiary(
        "/projects/" + this.props.location.state.project.name,
        body
      ).then(result => {
        this.props.reload();
      });
    }
  }

  clickActivate() {
    let body = {
      model_name: this.state.rowData.model_name,
      serving: true
    };

    BaseActions.putApiary(
      "/projects/" + this.props.location.state.project.name,
      body
    ).then(result => {
      this.props.reload();
    });
  }

  clickRetire() {
    let body = {
      model_name: this.state.rowData.model_name,
      serving: false
    };

    BaseActions.putApiary(
      "/projects/" + this.props.location.state.project.name,
      body
    ).then(result => {
      this.props.reload();
    });
  }

  render() {
    const { rowData, isDetail, isRecalibrate } = this.state;

    const promoteRetireText =
      rowData.status === "Active" ? "Retire" : "Promote";

    let detailAccordion = null;
    if (isDetail) {
      detailAccordion = <ModelManagementDetail model={rowData} />;
    }

    let recalibrateModal = null;
    if (isRecalibrate) {
      recalibrateModal = (
        <NewModelRecalibrationModal
          onClose={this.clickRecalibrate}
          model={rowData}
          reload={this.props.reload}
          {...this.props}
        />
      );
    }

    let entrypoints = "";

    for (var key in rowData.entrypoints) {
      entrypoints += key + ": ";
      for (var subkey in rowData.entrypoints[key]) {
        entrypoints += subkey + ": " + rowData.entrypoints[key][subkey] + " ";
      }
      entrypoints += "; ";
    }

    let validation_metric = "";

    if (rowData.validation_metrics) {
      for (var key in rowData.validation_metrics) {
        validation_metric +=
          key + ": " + rowData.validation_metrics[key] + "; ";
      }
    }

    return (
      <div className="model-management-row">
        <div className="model-management-cell">
          <input
            className="model-checkbox-default"
            type="checkbox"
            onClick={this.onChangeDefault}
            checked={rowData.default === true}
          />
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{rowData.model_name}</p>
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{rowData.created_at}</p>
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{rowData.created_by}</p>
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{rowData.description || ""}</p>
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{entrypoints}</p>
        </div>
        <div className="model-management-cell">
          <p
            className={
              rowData.status === "Active" ? "hide-text active" : "hide-text"
            }
          >
            {rowData.status}
          </p>
        </div>
        <div className="model-management-cell">
          <p className="hide-text">{validation_metric}</p>
        </div>
        <div className="model-management-cell">
          <div className="container-cell-buttons">
            <button
              className="b--secondary-text"
              onClick={this.clickRecalibrate}
            >
              recalibrate
            </button>
            <button
              className="b--secondary-text"
              onClick={
                rowData.status === "activated"
                  ? this.clickRetire
                  : this.clickActivate
              }
            >
              {rowData.status === "activated" ? "retire" : "activate"}
            </button>
            <button
              className={
                isDetail ? "b--secondary-text active" : "b--secondary-text"
              }
              onClick={this.clickDetails}
            >
              {isDetail ? <i class="arrow up" /> : <i class="arrow down" />}
              <span>details</span>
            </button>
          </div>
        </div>
        {detailAccordion}
        {recalibrateModal}
      </div>
    );
  }
}

ModelManagementRow.propTypes = {
  rowData: PropTypes.object,
  isDetail: PropTypes.bool,
  toggleDetailRow: PropTypes.func,
  rowNum: PropTypes.number,
  isRecalibrate: PropTypes.bool,
  location: PropTypes.object,
  reload: PropTypes.func
};

ModelManagementRow.defaultProps = {
  rowData: {},
  isDetail: false,
  toggleDetailRow: () => {},
  rowNum: -1,
  isRecalibrate: false
};

export default ModelManagementRow;
