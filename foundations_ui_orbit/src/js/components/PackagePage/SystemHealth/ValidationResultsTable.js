import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";

class ValidationResultsTable extends Component {
  constructor(props) {
    super(props);
    const { location } = this.props;

    this.state = {
      rows: null,
      projectName: location.state.project.name
    };
    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  async reload() {
    const { projectName } = this.state;
    const { onClickRow, reload } = this.props;

    const result = await ValidationResultsActions.getValidationResultList(projectName);
    const rows = ValidationResultsActions.getResultRows(result, onClickRow);
    this.setState({ rows: rows });
    reload();
  }

  render() {
    const { rows } = this.state;
    const { selectedRow } = this.props;

    let rowsWithProps = [];
    if (rows) {
      rowsWithProps = rows.map(row => React.cloneElement(
        row,
        { selectedRow: selectedRow }
      ));
    }

    return (
      <div className="validation-results-table-container">
        <div className="i--icon-refresh" title="Refresh validation results" onClick={this.reload} />
        <div className="validation-results-table-row-header">
          <div className="val-time-table-cell">Date</div>
          <div className="val-monitor-table-cell">Monitor Name</div>
          <div className="val-contract-table-cell">Contract Name</div>
          <div className="val-critical-table-cell" />
        </div>
        <div className="validation-results-table">
          {rowsWithProps}
        </div>
      </div>
    );
  }
}

ValidationResultsTable.propTypes = {
  location: PropTypes.object,
  onClickRow: PropTypes.func,
  selectedRow: PropTypes.object,
  reload: PropTypes.func
};

ValidationResultsTable.defaultProps = {
  location: { state: {} },
  onClickRow: () => {},
  selectedRow: {},
  reload: () => {}
};

export default ValidationResultsTable;
