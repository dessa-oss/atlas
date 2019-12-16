import React from 'react';
import PropTypes from 'prop-types';
import { getAtlas } from '../../../actions/BaseActions';

class MonitorLogs extends React.Component {
  constructor(props) {
    super(props);

    this.state = { message: '' };

    this.reload = this.reload.bind(this);
  }

  componentDidMount() {
    this.reload();
  }

  componentDidUpdate(prevProps) {
    const { jobID, projectName } = this.props;
    if (jobID !== prevProps.jobID || projectName !== prevProps.projectName) {
      this.reload();
    }
  }

  reload() {
    const { jobID, projectName } = this.props;

    if (jobID && projectName) {
      getAtlas(`projects/${projectName}/job_listing/${jobID}/logs`)
        .then(result => {
          this.setState({
            message: result.log,
          });
        });
    }
  }

  render() {
    const { message } = this.state;

    return (
      <div className="monitor-logs-modal-container-logs">
        {message}
      </div>
    );
  }
}


MonitorLogs.propTypes = {
  jobID: PropTypes.string,
  projectName: PropTypes.string,
};

MonitorLogs.defaultProps = {
  jobID: '',
  projectName: '',
};

export default MonitorLogs;
