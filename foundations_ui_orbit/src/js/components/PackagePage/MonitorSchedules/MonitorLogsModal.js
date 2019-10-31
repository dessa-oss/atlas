import React from "react";
import { Modal, ModalBody } from "reactstrap";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import MonitorLogs from "./MonitorLogs";

class MonitorLogsModal extends React.Component {
  constructor(props) {
    super(props);
    this.onToggleModal = this.onToggleModal.bind(this);
  }

  onToggleModal() {
    const { toggle } = this.props;
    toggle(null);
  }

  render() {
    const {
      isOpen,
      toggle,
      jobID,
      projectName
    } = this.props;

    return (
      <Modal
        isOpen={isOpen}
        toggle={this.onToggleModal}
        className="modal-job-details"
      >
        <ModalBody>
          <div className="contanier-main">
            <div className="container-title">
              <p className="label-id">Details For Job</p>
              <div className="container-id">
                <p className="text-id">{jobID}</p>
              </div>
              <div
                className="close"
                onClick={this.onToggleModal}
                role="button"
                aria-label="Close"
                tabIndex={0}
              />
            </div>
            <MonitorLogs jobID={jobID} projectName={projectName} />
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


MonitorLogsModal.propTypes = {
  isOpen: PropTypes.bool,
  toggle: PropTypes.func,
  jobID: PropTypes.string,
  projectName: PropTypes.string
};

MonitorLogsModal.defaultProps = {
  isOpen: false,
  toggle: () => {},
  jobID: "",
  projectName: ""
};

export default withRouter(MonitorLogsModal);
