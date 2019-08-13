import React, { Component } from "react";
import PropTypes from "prop-types";
import ProjectPage from "./ProjectPage/ProjectPage";
import NewDeployment from "./PackagePage/NewDeployment";

class App extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.props.history.push("/projects");
  }

  render() {
    return <div />;
  }
}

App.propTypes = {};

App.defaultProps = {};

export default App;
