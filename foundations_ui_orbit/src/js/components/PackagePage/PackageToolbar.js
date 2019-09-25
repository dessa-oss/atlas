import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PackagePageHeader from "./PackagePageHeader";
import { get, getMaster, postMaster } from "../../actions/BaseActions";
import moment from "moment";

const PackageToolbar = props => {
  const [demoOpen, setDemoOpen] = React.useState(true);
  const [selectedDate, setSelectedDate] = React.useState("");
  const [resetting, setResetting] = React.useState(false);
  const [attribute, setAttribute] = React.useState("");

  const reload = () => {
    getMaster("simulator/get_date").then(result => {
      let formattedDate = moment(result.current_date).format("YYYY-MM-DD").toString();

      setSelectedDate(formattedDate);
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onClickOpenDemo = () => {
    setDemoOpen(true);
  };

  const onClickCloseDemo = () => {
    setDemoOpen(false);
  };

  const onChangeAttribute = e => {
    setAttribute(e.target.value);
  };

  const onClickReset = () => {
    postMaster("simulator_admin/restart", {})
      .then(() => {
        reload();
      });
  };

  const onClickSendIssue = () => {
    if (attribute !== "") {
      setResetting(true);

      getMaster(`simulator/fix_special_value?column_name=${attribute}`)
        .then(() => {
          setResetting(false);
          reload();
        })
        .catch(() => {
          setResetting(false);
        });
    }
  };

  const { project, title, openTutorial } = props;

  return (
    <div className="layout-package-toolbar-container">
      <div className="job-header-logo-container">
        <div className="i--icon-logo" />
        <PackagePageHeader
          pageName={project.name}
          pageSubName={
            title === ""
              ? "Inference Automation and Model Management"
              : title
          }
        />
        <div className="icon-tutorial" onClick={openTutorial}>
          <p>?</p>
        </div>
        {demoOpen === true ? (
          <div className="container-layout-demo">
            <div className="container-demo-arrow">
              <i
                className="arrow right demo-icon-arrow"
                onClick={onClickCloseDemo}
              />
            </div>
            {resetting === true && (
              <div className="container-resetting">
                <p>Request sent. This might take a moment.</p>
              </div>
            )}
            {resetting === false && (
              <div className="container-demo-actions">
                <div className="container-reset">
                  <p className="label-date">{selectedDate}</p>
                  <button type="button" className="b--secondary-text button-reset" onClick={onClickReset}>
                    RESET TRIAL
                  </button>
                </div>
                <div className="container-issue">
                  <p>Report Data Issue</p>
                  <input value={attribute} placeholder="Attribute name" onChange={onChangeAttribute} />
                  <button type="button" className="b--secondary-text button-reset" onClick={onClickSendIssue}>
                    SEND
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="container-layout-demo hidden">
            <i
              className="arrow left demo-icon-arrow-left"
              onClick={onClickOpenDemo}
            />
          </div>
        )}
      </div>
    </div>
  );
};

PackageToolbar.propTypes = {
  project: PropTypes.object,
  title: PropTypes.string,
  onLoading: PropTypes.func,
  openTutorial: PropTypes.func
};

PackageToolbar.defaultProps = {
  project: {},
  title: "",
  onLoading: () => null,
  openTutorial: () => null
};

export default withRouter(PackageToolbar);
