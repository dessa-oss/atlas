import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import { CopyToClipboard } from "react-copy-to-clipboard";
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
      jobID,
      projectName
    } = this.props;

    return (
      <Modal
        isOpen={isOpen}
        toggle={this.onToggleModal}
        className="monitor-logs-modal"
        fade={false}
      >
        <ModalBody>
          <div className="monitor-logs-modal-container-main">
            <div className="monitor-logs-modal-container-title">
              <p className="monitor-logs-modal-label-id">Details For Job</p>
              <div className="monitor-logs-modal-container-id">
                <p className="monitor-logs-modal-text-id">{jobID}</p>
                <CopyToClipboard text={jobID}>
                  <span
                    onClick={this.notifiedCopy}
                    className="i--icon-copy"
                    role="presentation"
                  />
                </CopyToClipboard>
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
