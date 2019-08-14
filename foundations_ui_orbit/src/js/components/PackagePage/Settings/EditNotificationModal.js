import React, { Component } from "react";
import PropTypes from "prop-types";
import Select from "react-select";
import MultiSelect from "@kenshooui/react-multi-select";
import "@kenshooui/react-multi-select/dist/style.css";
import BaseActions from "../../../actions/BaseActions";

const conditionOptions = [
  { value: "Errors Only", label: "Errors Only" },
  { value: "All Updates", label: "All Updates" }
];

class EditNotification extends Component {
  constructor(props) {
    super(props);
    this.state = {
      category: this.props.category,
      updateNotifications: this.props.updateNotifications,
      allUsers: this.props.allUsers,
      condition: "Errors Only",
      selectedUsers: []
    };
    this.UpdateNotification = this.UpdateNotification.bind(this);
    this.ChangeUsers = this.ChangeUsers.bind(this);
    this.ChangeCondtion = this.ChangeCondtion.bind(this);
  }

  async UpdateNotification() {
    const {
      condition,
      selectedUsers,
      category,
      updateNotifications
    } = this.state;

    const data = {
      condition: condition,
      recipients: selectedUsers,
      category: category
    };

    const body = JSON.stringify(data);

    await BaseActions.postJSONFile(
      "settings/users/notification",
      "notifications.json",
      body
    );

    updateNotifications();
  }

  ChangeUsers(selectedOptions) {
    const selectedUsers = selectedOptions.map(option => {
      return option.label;
    });
    this.setState({ selectedUsers: selectedUsers });
  }

  ChangeCondtion(selectedOption) {
    this.setState({ condition: selectedOption.value });
  }

  render() {
    const { allUsers } = this.state;
    return (
      <div className="edit-notificaiton-modal-container">
        <div>
          <p className="edit-notification font-bold">Condition:</p>
          <div className="edit-notification-select-condition">
            <Select options={conditionOptions} onChange={this.ChangeCondtion} />
          </div>
        </div>
        <div className="multi-select-container">
          <p className="add-user-modal-label font-bold edit-not-subtitle">
            Recipients:
          </p>
          <div className="edit-notificaiton-multi-select-container">
            <MultiSelect
              items={allUsers}
              wrapperClassName={"edit-notification-multi-select"}
              onChange={this.ChangeUsers}
            />
          </div>
        </div>
        <button
          type="button"
          onClick={this.UpdateNotification}
          className="b--mat b--affirmative text-upper"
        >
          update notification
        </button>
      </div>
    );
  }
}

EditNotification.propTypes = {
  category: PropTypes.string
};

EditNotification.defaultProps = {};

export default EditNotification;
