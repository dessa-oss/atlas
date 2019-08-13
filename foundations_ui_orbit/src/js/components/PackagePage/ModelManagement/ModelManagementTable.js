import React, { Component } from "react";
import PropTypes from "prop-types";
import ModelManagementRow from "./ModelManagementRow";

const ModelManagementTable = props => {
  const [detailRow, setDetailRow] = React.useState(-1);

  const toggleDetailRow = rowNum => {
    setDetailRow(rowNum);
  };

  const renderRows = () => {
    let rows = [];
    let curRow = 0;
    props.tableData.forEach(row => {
      const isDetail = curRow === detailRow ? true : false;
      rows.push(
        <ModelManagementRow
          key={curRow}
          rowData={row}
          rowNum={curRow}
          isDetail={isDetail}
          toggleDetailRow={toggleDetailRow}
          reload={props.reload}
          {...props}
        />
      );
      curRow++;
    });

    return rows;
  };

  return (
    <div className="model-management-container no-horizontal-scroll">
      <div className="model-management-header-container">
        <div className="model-management-header">
          <p className="font-bold">Default</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Model Deployed</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Created On</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Created By</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Description</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Entrypoints</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Status</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Validation Metric</p>
        </div>
        <div className="model-management-header button-width" />
      </div>
      <div className="model-management-row-container">{renderRows()}</div>
    </div>
  );
};

ModelManagementTable.propTypes = {
  tableData: PropTypes.array,
  detailRow: PropTypes.number,
  reload: PropTypes.func
};

ModelManagementTable.defaultProps = {
  tableData: [],
  detailRow: -1
};

export default ModelManagementTable;
