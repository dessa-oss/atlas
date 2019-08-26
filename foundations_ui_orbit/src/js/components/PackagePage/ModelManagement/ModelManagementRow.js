import React from "react";
import PropTypes from "prop-types";
import ModelManagementDetail from "./ModelManagementDetails";
import { putApiary } from "../../../actions/BaseActions";
import NewModelRecalibrationModal from "./NewModelRecalibrationModal";

const ModelManagementRow = props => {
  const [recalibrateOpen, setRecalibrateOpen] = React.useState(false);

  const clickDetails = () => {
    const { isDetail, toggleDetailRow, rowNum } = props;

    if (isDetail) {
      toggleDetailRow(-1);
    } else {
      toggleDetailRow(rowNum);
    }
  };

  const clickRecalibrate = () => {
    const value = !recalibrateOpen;
    setRecalibrateOpen(value);
  };

  const onChangeDefault = () => {
    const { rowData, location, reload } = props;

    if (rowData.default === false) {
      const body = {
        default_model: rowData.model_name
      };

      putApiary(
        `/projects/${location.state.project.name}`,
        body
      ).then(() => {
        reload();
      });
    }
  };

  const clickActivate = () => {
    const { rowData, location, reload } = props;

    const body = {
      model_name: rowData.model_name,
      serving: true
    };

    putApiary(
      `/projects/${location.state.project.name}`,
      body
    ).then(() => {
      reload();
    });
  };

  const clickRetire = () => {
    const { rowData, location, reload } = props;

    const body = {
      model_name: rowData.model_name,
      serving: false
    };

    putApiary(
      `/projects/${location.state.project.name}`,
      body
    ).then(() => {
      reload();
    });
  };

  const { rowData, isDetail, reload } = props;

  return (
    <div className="model-management-row">
      <div className="model-management-cell">
        <input
          className="model-checkbox-default"
          type="checkbox"
          onClick={onChangeDefault}
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
        <p
          className={
            rowData.status === "Active" ? "hide-text active" : "hide-text"
          }
        >
          {rowData.status}
        </p>
      </div>
      <div className="model-management-cell">
        <div className="container-cell-buttons">
          <button type="button" className="b--secondary-text button-management" onClick={clickRecalibrate}>
            recalibrate
          </button>
          <button
            type="button"
            className="b--secondary-text button-management"
            onClick={
              rowData.status === "activated" ? clickRetire : clickActivate
            }
          >
            {rowData.status === "activated" ? "deactivate" : "activate"}
          </button>
          <button
            type="button"
            className={
              isDetail ? "b--secondary-text button-management active" : "b--secondary-text button-management"
            }
            onClick={clickDetails}
          >
            {isDetail === true ? (
              <i className="arrow up" />
            ) : (
              <i className="arrow down" />
            )}
            <span>details</span>
          </button>
        </div>
      </div>
      {isDetail === true && (
        <ModelManagementDetail model={rowData} />
      )}
      {recalibrateOpen === true && (
        <NewModelRecalibrationModal
          onClose={clickRecalibrate}
          model={rowData}
          reload={reload}
          {...props}
        />
      )}
    </div>
  );
};

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
  toggleDetailRow: () => { },
  rowNum: -1,
  isRecalibrate: false,
  location: { state: {} },
  reload: () => null
};

export default ModelManagementRow;
