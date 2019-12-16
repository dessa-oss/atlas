import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import Layout from '../Layout';
import PropTypes from 'prop-types';
import ModalTutorial from '../../common/ModalTutorial';
import ValidationResultsTable from './ValidationResultsTable';
import ValidationResultsDetails from './ValidationResultsDetails';
import DataContractInfoModal from './DataContractInfoModal';

class SystemHealth extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedValidationResult: {},
      tutorialVisible: false,
      selectedUuid: '',
      infoVisible: false,
    };

    this.selectRow = this.selectRow.bind(this);
    this.reload = this.reload.bind(this);
    this.onToggleTutorial = this.onToggleTutorial.bind(this);
    this.onToggleDataContractInfo = this.onToggleDataContractInfo.bind(this);
  }

  selectRow(selectedResult) {
    this.setState({ selectedValidationResult: selectedResult });
  }

  reload() {
    this.setState({ selectedValidationResult: {} });
  }

  onToggleTutorial() {
    const { tutorialVisible } = this.state;
    this.setState({ tutorialVisible: !tutorialVisible });
  }

  onToggleDataContractInfo(uuid) {
    const { infoVisible } = this.state;
    this.setState({ infoVisible: !infoVisible, selectedUuid: uuid });
  }

  render() {
    const {
      selectedValidationResult,
      selectedUuid,
      tutorialVisible,
      infoVisible,
    } = this.state;

    const { location } = this.props;

    return (
      <Layout tab="Health" title="Data Health" openTutorial={this.onToggleTutorial}>
        <div className="new-systemhealth-container-deployment">
          <div className="main-display-data-health">
            <div className="new-systemhealth-section font-bold">
              Data Validation Results
            </div>
            <div className="systemhealth-body">
              <div className="left-side">
                <ValidationResultsTable
                  location={location}
                  onClickRow={this.selectRow}
                  selectedRow={selectedValidationResult}
                  reload={this.reload}
                />
              </div>
              <div className="right-side">
                <ValidationResultsDetails
                  location={location}
                  selectedValidationResult={selectedValidationResult}
                  toggleInfo={this.onToggleDataContractInfo}
                />
              </div>
            </div>
          </div>
          <ModalTutorial
            tutorialVisible={tutorialVisible}
            onToggleTutorial={this.onToggleTutorial}
          />
          <DataContractInfoModal
            isOpen={infoVisible}
            toggle={this.onToggleDataContractInfo}
            uuid={selectedUuid}
          />
        </div>
      </Layout>
    );
  }
}

SystemHealth.propTypes = {
  location: PropTypes.object,
};

SystemHealth.defaultProps = {
  location: { state: {} },
};

export default withRouter(SystemHealth);
