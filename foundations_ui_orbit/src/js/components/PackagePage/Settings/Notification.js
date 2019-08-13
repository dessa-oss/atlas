import React, { Component } from "react";
import PropTypes from "prop-types";
import EditNotificationModal from './EditNotificationModal';
import { Modal, ModalBody } from "reactstrap";

class Notification extends Component {
  constructor(props) {
    super(props);
    this.state = {
      category: this.props.category,
      condition: this.props.condition,
      recipients: this.props.recipients,
      isShowingEditNotification: false,
      emails: this.props.emails,
      updateNotifications: this.props.updateNotifications,
    };
    this.editNotification = this.editNotification.bind(this);
    this.toggleShowEditNotification = this.toggleShowEditNotification.bind(this);
  }

  editNotification() {
    const { updateNotifications } = this.state;
    updateNotifications();
    this.setState({isShowingEditNotification: false});
  }

  toggleShowEditNotification() {
    const {isShowingEditNotification} = this.state
    this.setState({isShowingEditNotification: !isShowingEditNotification});
  }

  render() {
    const { category, recipients, isShowingEditNotification, emails } = this.state;

    return (
      <div className="notification-container">
        <div className="notification-category">
          <p>{category}</p>
        </div>
        <div className="notification-recipients">
          <p>{recipients.join(", ")}</p>
        </div>
        <div className="notification-edit">
          <button className="b--secondary" onClick={this.toggleShowEditNotification}>
            <div className="i--icon-pencil-grey" />
          </button>
        </div>
        <Modal
          isOpen={isShowingEditNotification}
          toggle={this.toggleShowEditNotification}
          className={"settings-add-user-modal-container notification"}
        >
          <ModalBody>
            <EditNotificationModal updateNotifications={this.editNotification} allUsers={emails} selectedUsers={recipients} category={category} />
          </ModalBody>
        </Modal>
      </div>
    );
  }
}

Notification.propTypes = {
};

Notification.defaultProps = {
};

export default Notification;
