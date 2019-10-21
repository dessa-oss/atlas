import React, { Component } from "react";
import PropTypes from "prop-types";
import ValidationResultsActions from "../../../actions/ValidationResultsActions";
import ValidationResultsOverview from "./ValidationResultsOverview";
import ValidationResultsTests from "./ValidationResultsTests";
import CommonActions from "../../../actions/CommonActions";

class ValidationResultsDetails extends Component {
  constructor(props) {
    super(props);

    this.state = {
      validationResult: {}
    };

    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    if (!CommonActions.deepEqual(this.props.selectedValidationResult, prevProps.selectedValidationResult)) {
      this.reload();
    }
  }

  async reload() {
    const { location, selectedValidationResult } = this.props;

    if (location && !CommonActions.isEmptyObject(selectedValidationResult)) {
      const validationResult = await ValidationResultsActions.getValidationResults(
        location.state.project.name,
        selectedValidationResult.time,
        selectedValidationResult.monitorName,
        selectedValidationResult.contractName
      );
      this.setState({ validationResult: validationResult });
    }
  }

  render() {
    const { validationResult } = this.state;

    let mainRender = (
      <div className="validation-results-details">
        <ValidationResultsOverview validationResult={validationResult} />
        <ValidationResultsTests />
      </div>
    );
    if (!validationResult || CommonActions.isEmptyObject(validationResult)) {
      mainRender = <div className="validation-results-details">add empty state</div>;
    }

    return mainRender;
  }
}

ValidationResultsDetails.propTypes = {
  location: PropTypes.object,
  selectedValidationResult: PropTypes.object
};

ValidationResultsDetails.defaultProps = {
  location: {},
  selectedValidationResult: {}
};

export default ValidationResultsDetails;
