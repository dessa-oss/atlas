import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PackagePageHeader from "./PackagePageHeader";
import { get, getMaster, postMaster } from "../../actions/BaseActions";
import moment from "moment";

class PackageToolbar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      demoOpen: true,
      selectedDate: "",
      resetting: false,
      attribute: "",
      timerId: -1
    };

    this.onClickOpenDemo = this.onClickOpenDemo.bind(this);
    this.onClickCloseDemo = this.onClickCloseDemo.bind(this);
    this.onClickReset = this.onClickReset.bind(this);
    this.onClickSendIssue = this.onClickSendIssue.bind(this);
    this.onChangeAttribute = this.onChangeAttribute.bind(this);
  }

  reload() {
    getMaster("simulator/get_date").then(result => {
      let formattedDate = moment(result.current_date).format("YYYY-MM-DD").toString();

      this.setState({
        selectedDate: formattedDate
      });
    });
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 30000);
    this.setState({
      timerId: value
    });
  }

  clearTimer() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  componentWillUnmount() {
    this.clearTimer();
  }

  onClickOpenDemo() {
    this.setState({
      demoOpen: true
    });
  }

  onClickCloseDemo() {
    this.setState({
      demoOpen: false
    });
  }

  onChangeAttribute(e) {
    this.setState({
      attribute: e.target.value
    });
  }

  onClickReset() {
    postMaster("simulator_admin/restart", {})
      .then(() => {
        this.reload();
      });
  }

  onClickSendIssue() {
    const { attribute } = this.state;
    if (attribute !== "") {
      this.setState({
        resetting: true
      });

      getMaster(`simulator/fix_special_value?column_name=${attribute}`)
        .then(() => {
          this.setState({
            resetting: false
          });
          this.reload();
        })
        .catch(() => {
          this.setState({
            resetting: false
          });
        });
    }
  }

  render() {
    const { project, title, openTutorial } = this.props;
    const {
      demoOpen, resetting, selectedDate, attribute
    } = this.state;

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
                  onClick={this.onClickCloseDemo}
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
                    <button type="button" className="b--secondary-text button-reset" onClick={this.onClickReset}>
                      RESET TRIAL
                    </button>
                  </div>
                  <div className="container-issue">
                    <p>Report Data Issue</p>
                    <input value={attribute} placeholder="Attribute name" onChange={this.onChangeAttribute} />
                    <button type="button" className="b--secondary-text button-reset" onClick={this.onClickSendIssue}>
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
                onClick={this.onClickOpenDemo}
              />
            </div>
          )}
        </div>
      </div>
    );
  }
}

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
