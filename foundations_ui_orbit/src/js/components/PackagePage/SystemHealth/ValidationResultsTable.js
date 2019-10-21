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
    const { onClickRow } = this.props;

    const result = await ValidationResultsActions.getValidationResultList(projectName);
    const rows = ValidationResultsActions.getRows(result, onClickRow);
    this.setState({ rows: rows });
  }

  render() {
    const { rows } = this.state;

    return (
      <div className="validation-results-table">
        {rows}
      </div>
    );
  }
}

ValidationResultsTable.propTypes = {
  location: PropTypes.object,
  onClickRow: PropTypes.func
};

ValidationResultsTable.defaultProps = {
  location: { state: {} },
  onClickRow: () => {}
};

export default ValidationResultsTable;
