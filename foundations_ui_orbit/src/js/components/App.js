import React, { Component } from "react";
import ProptTypes from "prop-types";

class App extends Component {
  componentDidMount() {
    const { history } = this.props;

    history.push("/projects");
  }

  render() {
    return <div />;
  }
}

App.propTypes = {
  history: ProptTypes.object
};

App.defaultProps = {
  history: {}
};

export default App;
