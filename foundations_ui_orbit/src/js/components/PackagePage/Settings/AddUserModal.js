import React, { Component } from "react";
import PropTypes from "prop-types";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";

const roleOptions = [
  { value: "Admin", label: "Admin" },
  { value: "Manager", label: "Manager" },
  { value: "Read", label: "Read Only" }
];

class AddUserModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      updateUser: this.props.updateUser,
      role: null
    };
    this.AddUser = this.AddUser.bind(this);
    this.ChangeRole = this.ChangeRole.bind(this);
  }

  ChangeRole(selectedOption) {
    this.setState({ role: selectedOption.value });
  }

  async AddUser() {
    const { updateUser, role } = this.state;

    const name = document.getElementById("add-user-name").value;
    const id = document.getElementById("add-user-username").value;
    const email = document.getElementById("add-user-email").value;

    if (name !== "" && id !== "" && email !== "" && role !== null) {
      const data = {
        name: name,
        id: id,
        email: email,
        permission: role
      };

      const body = JSON.stringify(data);

      await BaseActions.postJSONFile("settings/users/add", "users.json", body);
      updateUser();
    }
  }

  render() {
    return (
      <div>
        <div>
          <p className="add-user-modal-label font-bold">Name:</p>
          <input id="add-user-name" />
        </div>
        <div>
          <p className="add-user-modal-label font-bold">Username:</p>
          <input id="add-user-username" />
        </div>
        <div>
          <p className="add-user-modal-label font-bold">Email:</p>
          <input id="add-user-email" />
        </div>
        <div>
          <p className="add-user-modal-label font-bold add-user-role-label">
            Role:
          </p>
          <div className="add-user-select-role">
            <Select options={roleOptions} onChange={this.ChangeRole} />
          </div>
        </div>
        <button
          type="button"
          onClick={this.AddUser}
          className="b--mat b--affirmative text-upper"
        >
          add user
        </button>
      </div>
    );
  }
}

AddUserModal.propTypes = {
  updateUser: PropTypes.func
};

AddUserModal.defaultProps = {};

export default AddUserModal;
