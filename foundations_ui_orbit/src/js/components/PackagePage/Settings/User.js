import React from "react";
import PropTypes from "prop-types";
import { postJSONFile } from "../../../actions/BaseActions";

const roleOptions = [
  { value: "Admin", label: "Admin" },
  { value: "Manager", label: "Manager" },
  { value: "Read", label: "Read" }
];

class User extends React.Component {
  constructor(props) {
    super(props);

    const {
      name, username, email, role
    } = this.props;

    this.state = {
      name: name,
      username: username,
      email: email,
      role: role
    };
    this.changeRole = this.changeRole.bind(this);
    this.deleteUser = this.deleteUser.bind(this);
  }

  async changeRole(selectedOption) {
    const {
      name, username, email, updateUser
    } = this.state;

    const data = {
      name: name,
      id: username,
      email: email,
      permission: selectedOption.target.value
    };

    const body = JSON.stringify(data);

    await postJSONFile("settings/users/role", "users.json", body);
    updateUser();
  }

  async deleteUser() {
    const { updateUser } = this.props;
    const { username } = this.state;
    await postJSONFile(
      "settings/users/delete",
      "users.json",
      username
    );
    updateUser();
  }

  render() {
    const {
      name, username, email, role
    } = this.state;

    return (
      <div className="user-container">
        <div className="user-name">
          <p>{name}</p>
        </div>
        <div className="user-username">
          <p>{username}</p>
        </div>
        <div className="user-email">
          <p>{email}</p>
        </div>
        <div className="user-select-role user-role">
          <select
            className="select-frequency adaptive"
            options={roleOptions}
            value={role}
            onChange={this.changeRole}
          >
            {roleOptions.map(item => {
              return <option key={item}>{item.label}</option>;
            })}
          </select>
        </div>
        <div className="user-delete">
          <button type="button" className="b--secondary red" onClick={this.deleteUser}>
            <div className="close" />
          </button>
        </div>
      </div>
    );
  }
}

User.propTypes = {
  name: PropTypes.string,
  username: PropTypes.string,
  email: PropTypes.string,
  role: PropTypes.string,
  updateUser: PropTypes.func
};

User.defaultProps = {
  name: "",
  username: "",
  email: "",
  role: "",
  updateUser: () => null
};

export default User;
