import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { Modal, ModalBody } from 'reactstrap';

class DeleteConfirmModal extends React.Component {
  constructor(props) {
    super(props);
    this.onToggleModal = this.onToggleModal.bind(this);
    this.onClickDelete = this.onClickDelete.bind(this);
  }

  onToggleModal() {
    const { toggle } = this.props;
    toggle(null);
  }

  onClickDelete() {
    const { onConfirm } = this.props;
    this.onToggleModal();
    onConfirm();
  }

  render() {
    const { isOpen } = this.props;

    return (
      <Modal
        isOpen={isOpen}
        toggle={this.onToggleModal}
        className="monitor-delete-modal"
        fade={false}
      >
        <ModalBody>
          <div className="monitor-delete-modal-main">
            <div className="i--icon-alert" />
            <div className="monitor-delete-modal-title">Are you sure?</div>
            <div className="monitor-delete-modal-body">
              Deleting a monitor will also delete all the associated jobs.
              This action cannot be undone.
            </div>
          </div>
          <div className="monitor-delete-modal-buttons">
            <div className="monitor-delete-modal-button-no" onClick={this.onToggleModal}>Cancel</div>
            <div className="monitor-delete-modal-button-yes" onClick={this.onClickDelete}>Delete</div>
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


DeleteConfirmModal.propTypes = {
  isOpen: PropTypes.bool,
  toggle: PropTypes.func,
  onConfirm: PropTypes.func,
};

DeleteConfirmModal.defaultProps = {
  isOpen: false,
  toggle: () => {},
  onConfirm: () => {},
};

export default withRouter(DeleteConfirmModal);
