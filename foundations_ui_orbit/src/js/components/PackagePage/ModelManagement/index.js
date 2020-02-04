import React from 'react';
import DefineNewModal from './DefineNewModal';
import { withRouter } from 'react-router-dom';
import Layout from '../Layout';
import { get, getFromApiary } from '../../../actions/BaseActions';
import { Modal, ModalBody } from 'reactstrap';
import ModelManagementTable from './ModelManagementTable';
import Schedule from './Schedule';
import ModalTutorial from '../../common/ModalTutorial';
import PropTypes from 'prop-types';

class ModelManagement extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modelManagementData: [],
      open: false,
      tutorialVisible: false,
      timerId: -1,
    };

    this.onClickOpenDefineNew = this.onClickOpenDefineNew.bind(this);
    this.onClickCloseDefineNew = this.onClickCloseDefineNew.bind(this);
    this.onToggleTutorial = this.onToggleTutorial.bind(this);
    this.startTimer = this.startTimer.bind(this);
    this.stopTimer = this.stopTimer.bind(this);
  }

  reload() {
    const { location } = this.props;
    getFromApiary(
      `projects/${location.state.project.name}/model_listing`,
    ).then(result => {
      if (result) {
        this.setState({
          modelManagementData: result.models,
        });
      }
    });
  }

  startTimer() {
    const id = setInterval(() => {
      this.reload();
    }, 10000);
    this.setState({
      timerId: id,
    });
  }

  stopTimer() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  componentDidMount() {
    this.reload();
    this.startTimer();
  }

  componentWillUnmount() {
    this.stopTimer();
  }

  onClickOpenDefineNew() {
    this.setState({
      open: true,
    });
  }

  onClickCloseDefineNew() {
    this.setState({
      open: false,
    });
    const id = setInterval(() => {
      this.reload();
    }, 1000);
    this.setState({
      timerId: id,
    });
  }

  onToggleTutorial() {
    const { tutorialVisible } = this.state;
    const value = !tutorialVisible;
    this.setState({
      tutorialVisible: value,
    });
  }

  render() {
    const {
      modelManagementData,
      open,
      tutorialVisible,
      timerId,
    } = this.state;

    return (
      <Layout tab="Management" title="Model Management" openTutorial={this.onToggleTutorial}>
        <div className="package-deployment-container">
          {modelManagementData.length > 0 ? (
            <div>
              <Schedule />
              <div className="package-deployment-table-container">
                <p className="new-dep-section font-bold management">MODEL REGISTRY</p>
                <div className="container-management-top-section text-right">
                  <button
                    type="button"
                    onClick={this.onClickOpenDefineNew}
                    className="b--mat button-management-load"
                    disabled
                  >
                    <i className="plus-button" />
                    Define New
                  </button>
                </div>
                <ModelManagementTable
                  tableData={modelManagementData}
                  reload={this.reload}
                  startTimer={this.startTimer}
                  stopTimer={this.stopTimer}
                  {...this.props}
                />
              </div>
              <Modal
                isOpen={open}
                toggle={this.onClickCloseDefineNew}
                className="define-new-modal-container"
              >
                <ModalBody>
                  <DefineNewModal onClickClose={this.onClickCloseDefineNew} />
                </ModalBody>
              </Modal>
            </div>
          ) : (
            <div className="container-management-empty">
              <p>You have not loaded any reports</p>
              <p>
                Adding a model package can only be done using the command line
                interface
              </p>
            </div>
          )}
          <ModalTutorial
            tutorialVisible={tutorialVisible}
            onToggleTutorial={this.onToggleTutorial}
          />
        </div>
      </Layout>
    );
  }
}

ModelManagement.propTypes = {
  location: PropTypes.object,
};

ModelManagement.defaultProps = {
  location: { state: {} },
};

export default withRouter(ModelManagement);
