import React from "react";
import PropTypes from "prop-types";
import ModelManagementRow from "./ModelManagementRow";

const ModelManagementTable = props => {
  const [detailRow, setDetailRow] = React.useState(-1);

  const toggleDetailRow = rowNum => {
    setDetailRow(rowNum);
  };

  const renderRows = () => {
    const rows = [];
    let curRow = 0;
    props.tableData.forEach(row => {
      const isDetail = curRow === detailRow;
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
      curRow += 1;
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
          <p className="font-bold">Model Package Name</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Created On</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Created By</p>
        </div>
        <div className="model-management-header">
          <p className="font-bold">Status</p>
        </div>
        <div className="model-management-header button-width" />
      </div>
      <div className="model-management-row-container">{renderRows()}</div>
    </div>
  );
};

ModelManagementTable.propTypes = {
  tableData: PropTypes.array,
  reload: PropTypes.func
};

ModelManagementTable.defaultProps = {
  tableData: [],
  reload: () => null
};

export default ModelManagementTable;
