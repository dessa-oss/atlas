import React, { Component } from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import Layout from "../Layout";
import BaseActions from "../../../actions/BaseActions";
import User from "./User";
import Notification from "./Notification";
import { Modal, ModalBody } from "reactstrap";
import AddUserModal from "./AddUserModal";

class Settings extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMount: false,
      isLoading: true,
      users: [],
      notifications: [],
      filteredUsers: [],
      searching: false,
      isShowingAddUser: false
    };
    this.getUsers = this.getUsers.bind(this);
    this.saveUsers = this.saveUsers.bind(this);
    this.getNotifications = this.getNotifications.bind(this);
    this.saveNotifications = this.saveNotifications.bind(this);
    this.searchUsers = this.searchUsers.bind(this);
    this.toggleShowAddUser = this.toggleShowAddUser.bind(this);
    this.getDistinctUserEmails = this.getDistinctUserEmails.bind(this);
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    await this.getUsers();
    await this.getNotifications();
    await this.setState({ isLoading: false });
  }

  async getUsers() {
    const apiUsers = await BaseActions.getFromApiary("settings/users");
    if (apiUsers) {
      await this.saveUsers(apiUsers);
    }
    this.setState({ isShowingAddUser: false });
  }

  async getNotifications() {
    const apiNotifications = await BaseActions.getFromApiary(
      "settings/notifications"
    );
    if (apiNotifications) await this.saveNotifications(apiNotifications);
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
  }

  saveUsers(users) {
    if (users.data && users.data.length > 0) {
      this.setState({ users: users.data });
    } else {
      this.setState({ users: [] });
    }
  }

  saveNotifications(notifications) {
    if (notifications.data && notifications.data.length > 0) {
      this.setState({ notifications: notifications.data });
    } else {
      this.setState({ notifications: [] });
    }
  }

  searchUsers(event) {
    const { users } = this.state;
    let searchText = event.target.value;
    let searching = true;
    let filteredUsers = users.filter(u => {
      return u.name.toLowerCase().includes(searchText.toLowerCase());
    });

    if (searchText.length === 0) {
      searching = false;
    }

    this.setState({ filteredUsers: filteredUsers, searching: searching });
  }

  toggleShowAddUser() {
    const { isShowingAddUser } = this.state;
    this.setState({ isShowingAddUser: !isShowingAddUser });
  }

  getDistinctUserEmails() {
    const { users } = this.state;

    const allEmails = users.map(user => user.email);
    const distinctEmails = [...new Set(allEmails)];

    const emails = distinctEmails.map((email, index) => {
      return { id: index, label: email };
    });

    return emails;
  }

  render() {
    const {
      users,
      isLoading,
      notifications,
      filteredUsers,
      searching,
      isShowingAddUser
    } = this.state;

    const userRows = [];

    !searching
      ? users.forEach(user => {
          userRows.push(
            <User
              key={user.id + "-" + user.permission}
              name={user.name}
              username={user.id}
              email={user.email}
              role={user.permission}
              updateUser={this.getUsers}
            />
          );
        })
      : filteredUsers.forEach(user => {
          userRows.push(
            <User
              key={user.id + "-" + user.permission}
              name={user.name}
              username={user.id}
              email={user.email}
              role={user.permission}
            />
          );
        });

    const notificationRows = [];

    notifications.forEach(notif => {
      notificationRows.push(
        <Notification
          key={
            notif.category +
            "-" +
            notif.condition +
            "-" +
            notif.recipients.join("-")
          }
          category={notif.category}
          condition={notif.condition}
          recipients={notif.recipients}
          emails={this.getDistinctUserEmails()}
          updateNotifications={this.getNotifications}
        />
      );
    });

    const userTable = isLoading ? (
      <p className="settings-loading-users">Loading Users</p>
    ) : (
      userRows
    );

    return (
      <Layout tab="Settings" title="Settings">
        <div className="settings-page-container">
          {/* <div className="settings-title-container">
            <p className="settings-title text-upper font-bold">users</p>
          </div>
          <div className="settings-user-button-container">
              <div className="settings-user-search-container">
                <input
                  className="settings-user-search"
                  onChange={this.searchUsers}
                />
                <div className="magnifying-glass settings-user-search-magnifying-glass" />
              </div>
              <div className="settings-add-user-container">
                <button
                  type="button"
                  className="b--mat b--affirmative text-upper settings-add-user"
                  onClick={this.toggleShowAddUser}
                >
                  <i className="plus-button" />
                  add user
                </button>
              </div>
            </div>
          <div className="settings-user-container">
            {userTable.length > 0 ? (
              <div className="table">
                <div className="settings-user-column-container">
                  <p className="settings-user-column font-bold">Name</p>
                  <p className="settings-user-column font-bold">Username</p>
                  <p className="settings-user-column font-bold">Email</p>
                  <p className="settings-user-column font-bold">Role</p>
                  <p className="settings-user-column" />
                </div>
                <div className="settings-user-rows">{userTable}</div>
              </div>
            ) : (
              <div className="container-users-empty">
                <p>There are currently no users</p>
              </div>
            )}
          </div> */}

          <div className="settings-title-container">
            <p className="settings-title text-upper font-bold">notifications</p>
          </div>
          {notificationRows.length > 0 ? (
            <div className="settings-notifications-container">
              <div className="settings-notifications-column-container">
                <p className="settings-notifications-column font-bold">
                  Category
                </p>
                <p className="settings-notifications-column font-bold">
                  Recipients
                </p>
                <p className="settings-notifications-column" />
              </div>
              <div className="settings-notifications-rows">
                {notificationRows}
              </div>
            </div>
          ) : (
            <div className="container-users-empty">
              <p>There are currently no notifications</p>
            </div>
          )}
        </div>
        <Modal
          isOpen={isShowingAddUser}
          toggle={this.toggleShowAddUser}
          className={"settings-add-user-modal-container"}
        >
          <ModalBody>
            <AddUserModal updateUser={this.getUsers} />
          </ModalBody>
        </Modal>
      </Layout>
    );
  }
}

Settings.propTypes = {};

Settings.defaultProps = {};

export default withRouter(Settings);
