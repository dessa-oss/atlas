import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router-dom";
import PackagePageHeader from "./PackagePageHeader";
import { get } from "../../actions/BaseActions";
import moment from "moment";

const PackageToolbar = props => {
  const [demoOpen, setDemoOpen] = React.useState(false);
  const [selectedDate, setSelectedDate] = React.useState("");

  const reload = () => {
    get("dates/inference").then(result => {
      let formattedDate = "July 12, 2019";

      if (result) {
        const items = result.data.length > 0 ? result.data : result.meta.fields;
        const sortedItems = items.sort((a, b) => {
          const date1 = new Date(a);
          const date2 = new Date(b);
          return date2 - date1;
        });
        formattedDate = moment(sortedItems[0])
          .format("MMMM Do, YYYY")
          .toString();
      }

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

  const onClickReset = () => {
    const { onLoading } = props;
    onLoading(true, "Demo resetting...");

    get("reset")
      .then(() => {
        onLoading(false, "");
        reload();
      })
      .catch(() => {
        onLoading(false, "");
      });
  };

  const onClickFastForward = () => {
    const { onLoading } = props;

    onLoading(true, "Fast forwarding...");

    get("fastforward")
      .then(() => {
        onLoading(false, "");
        reload();
      })
      .catch(() => {
        onLoading(false, "");
      });
  };

  const { project, title } = props;

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
        {demoOpen === true ? (
          <div className="container-layout-demo">
            <div className="container-demo-arrow">
              <i
                className="arrow right demo-icon-arrow"
                onClick={onClickCloseDemo}
              />
            </div>

            <div className="container-demo-actions">
              <p>Demo Management</p>
              <p>{selectedDate}</p>
              <div className="container-demo-buttons">
                <button type="button" className="b--secondary-text" onClick={onClickReset}>
                  RESET
                </button>
                <button
                  type="button"
                  className="b--secondary-text"
                  onClick={onClickFastForward}
                >
                  FAST FORWARD
                </button>
              </div>
            </div>
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
  onLoading: PropTypes.func
};

PackageToolbar.defaultProps = {
  project: {},
  title: "",
  onLoading: () => null
};

export default withRouter(PackageToolbar);
