import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import { getAtlas } from "../../../actions/BaseActions";
import { CopyToClipboard } from "react-copy-to-clipboard";
import ModalInfo from "../../common/ModalInfo";

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
        className="centered-modal"
        fade={false}
      >
        <ModalBody>
          <div className="centered-modal-container-main">
            <div className="centered-modal-container-title">
              <p className="centered-modal-label-id">Details For Job</p>
              <div className="centered-modal-container-id">
                <p className="centered-modal-text-id">{jobID}</p>
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
            <ModalInfo
              fetchInfo={() => getAtlas(`projects/${projectName}/job_listing/${jobID}/logs`).then(result => result.log)}
            />
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
