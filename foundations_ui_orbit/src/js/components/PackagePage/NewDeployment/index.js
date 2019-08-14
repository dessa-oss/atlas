import React from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import Metadata from "./Metadata";
import Content from "./Content";
import Schedule from "./Schedule";

const NewDeploymentPage = props => {
  const { tab } = props;

  return (
    <Layout tab={tab} title="Deployment">
      <div className="new-dep-container-deployment">
        <Schedule />
        <Content />
        <Metadata />
      </div>
    </Layout>
  );
};

NewDeploymentPage.propTypes = {
  tab: PropTypes.string
};

NewDeploymentPage.defaultProps = {
  tab: "Deployment"
};

export default withRouter(NewDeploymentPage);
