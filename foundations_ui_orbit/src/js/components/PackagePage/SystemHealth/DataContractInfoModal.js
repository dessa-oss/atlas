import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import { Modal, ModalBody } from 'reactstrap';
import ModalInfo from '../../common/ModalInfo';
import { get } from '../../../actions/BaseActions';

class DataContractInfoModal extends React.Component {
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
      uuid,
    } = this.props;

    return (
      <Modal
        isOpen={isOpen}
        toggle={this.onToggleModal}
        className="centered-modal"
        fade={false}
      >
        <ModalBody>
          <div className="centered-modal-container-main" data-cy="data-contract-info-modal">
            <div className="centered-modal-container-title">
              <div
                className="close"
                onClick={this.onToggleModal}
                role="button"
                aria-label="Close"
                tabIndex={0}
              />
            </div>
            <ModalInfo fetchInfo={() => get(`contracts/${uuid}`)} />
          </div>
        </ModalBody>
      </Modal>
    );
  }
}


DataContractInfoModal.propTypes = {
  isOpen: PropTypes.bool,
  toggle: PropTypes.func,
  uuid: PropTypes.string,
};

DataContractInfoModal.defaultProps = {
  isOpen: false,
  toggle: () => {},
  uuid: '',
};

export default withRouter(DataContractInfoModal);
