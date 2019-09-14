import React from 'react';
import PropTypes from 'prop-types';
import BaseActions from '../../actions/BaseActions';

class Logs extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      message: '',
      timerId: -1,
    };
  }

  reload() {
    const { job, location } = this.props;
    const { projectName } = this.props.match.params;
    let selectedProjectName = location.state && location.state.project ? location.state.project.name : projectName;
    BaseActions.getFromApiary(`projects/${selectedProjectName}/job_listing/${job.job_id}/logs`)
      .then((result) => {
        this.setState({
          message: result.log,
        });
      });
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 2000);
    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  render() {
    const { message } = this.state;
    return (
      <div className="container-logs">
        {message}
      </div>
    );
  }
}

Logs.propTypes = {
  job: PropTypes.object,
  location: PropTypes.object,
  match: PropTypes.object,
};

Logs.defaultProps = {
  job: {},
  location: { state: {} },
  match: { params: {} },
};

export default Logs;
