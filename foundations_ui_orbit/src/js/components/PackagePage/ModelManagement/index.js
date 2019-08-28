import React from "react";
import DefineNewModal from "./DefineNewModal";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import { get, getFromApiary } from "../../../actions/BaseActions";
import { Modal, ModalBody } from "reactstrap";
import ModelManagementTable from "./ModelManagementTable";
import Schedule from "./Schedule";
import ModalTutorial from "../../common/ModalTutorial";
import PropTypes from "prop-types";

const ModelManagement = props => {
  const [modelManagementData, setModelManagementData] = React.useState([]);
  const [open, setOpen] = React.useState(false);
  const [tutorialVisible, setTutorialVisible] = React.useState(false);

  const reload = () => {
    get(
      `projects/${props.location.state.project.name}/model_listing`
    ).then(result => {
      if (result) {
        setModelManagementData(result.models);
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onClickOpenDefineNew = () => {
    setOpen(true);
  };

  const onClickCloseDefineNew = () => {
    setOpen(false);
  };

  const onToggleTutorial = () => {
    let value = !tutorialVisible;
    setTutorialVisible(value);
  };

  return (
    <Layout tab="Management" title="Model Management" openTutorial={onToggleTutorial}>
      <div className="package-deployment-container">
        {modelManagementData.length > 0 ? (
          <div>
            <Schedule />
            <div className="package-deployment-table-container">
              <p className="new-dep-section font-bold management">MODEL REGISTRY</p>
              <div className="container-management-top-section text-right">
                <button
                  type="button"
                  onClick={onClickOpenDefineNew}
                  className="b--mat b--affirmative button-management-load"
                >
                  <i className="plus-button" />
                  Define New
                </button>
              </div>
              <ModelManagementTable
                tableData={modelManagementData}
                reload={reload}
                {...props}
              />
            </div>
            <Modal
              isOpen={open}
              toggle={onClickCloseDefineNew}
              className="define-new-modal-container"
            >
              <ModalBody>
                <DefineNewModal onClickClose={onClickCloseDefineNew} />
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
          onToggleTutorial={onToggleTutorial}
        />
      </div>
    </Layout>
  );
};

ModelManagement.propTypes = {
  location: PropTypes.object
};

ModelManagement.defaultProps = {
  location: { state: {} }
};

export default withRouter(ModelManagement);
