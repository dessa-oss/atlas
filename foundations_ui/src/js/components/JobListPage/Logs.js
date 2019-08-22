import React from 'react';
import PropTypes from 'prop-types';
import BaseActions from '../../actions/BaseActions';

class Logs extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      message: '',
    };
  }

  componentDidMount() {
    const { job, location } = this.props;
    BaseActions.getFromApiary(`projects/${location.state.project.name}/job_listing/${job.job_id}/logs`)
      .then((result) => {
        this.setState({
          message: result.log,
        });
      });
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
};

Logs.defaultProps = {
  job: {},
  location: { state: {} },
};

export default Logs;
