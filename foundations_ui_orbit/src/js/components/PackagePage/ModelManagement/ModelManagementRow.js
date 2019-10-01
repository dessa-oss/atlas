import React from "react";
import PropTypes from "prop-types";
import ModelManagementDetail from "./ModelManagementDetails";
import { put } from "../../../actions/BaseActions";
import NewModelRecalibrationModal from "./NewModelRecalibrationModal";
import moment from "moment";


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

    const { stopTimer, startTimer } = props;
    if (value === true) {
      stopTimer();
    } else {
      startTimer();
    }
  };

  const onChangeDefault = () => {
    const { rowData, location, reload } = props;

    if (rowData.default === false) {
      const body = {
        default_model: rowData.model_name
      };

      put(
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

    put(
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

    put(
      `/projects/${location.state.project.name}`,
      body
    ).then(() => {
      reload();
    });
  };

  const { rowData, isDetail, reload } = props;
  const convertedDate = moment.unix(rowData.created_at).format("YYYY-MM-DD HH:mm").toString();

  return (
    <div className="model-management-row">
      <div className="model-management-cell">
        <input
          className="model-checkbox-default"
          type="radio"
          onClick={onChangeDefault}
          checked={rowData.default === true}
        />
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{rowData.model_name}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{convertedDate}</p>
      </div>
      <div className="model-management-cell">
        <p className="hide-text">{rowData.created_by}</p>
      </div>
      <div className="model-management-cell">
        <p
          className={
            rowData.status === "activated" ? "hide-text status-text active" : "hide-text status-text"
          }
        >
          {rowData.status}
        </p>
        <div className={rowData.status === "activated"
          ? "model-status-circle active"
          : "model-status-circle"}
        />
      </div>
      <div
        className={isDetail === true ? "model-management-cell last-child-details-open"
          : "model-management-cell"}
      >
        <div className="container-cell-buttons">
          <button type="button" className="b--secondary-text button-management recalibrate" onClick={clickRecalibrate}>
            recalibrate
          </button>
          <button
            type="button"
            className={rowData.status === "activated"
              ? "b--secondary-text button-management deactivate"
              : "b--secondary-text button-management activate"
            }
            onClick={
              rowData.status === "activated" ? clickRetire : clickActivate
            }
          >
            {rowData.status === "activated" ? "deactivate" : "activate"}
          </button>
          <button
            type="button"
            className={
              isDetail
                ? "b--secondary-text button-management details active"
                : "b--secondary-text button-management details"
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
          isOpen={recalibrateOpen}
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
  reload: PropTypes.func,
  startTimer: PropTypes.func,
  stopTimer: PropTypes.func
};

ModelManagementRow.defaultProps = {
  rowData: {},
  isDetail: false,
  toggleDetailRow: () => { },
  rowNum: -1,
  isRecalibrate: false,
  location: { state: {} },
  reload: () => null,
  startTimer: () => null,
  stopTimer: () => null
};

export default ModelManagementRow;
