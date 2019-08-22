import React from 'react';
import PropTypes from 'prop-types';
import { ScrollSyncPane } from 'react-scroll-sync';
import CommonActions from '../../actions/CommonActions';

class PopUpRows extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      jobs: this.props.jobs,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        jobs: nextProps.jobs,
      },
    );
  }

  render() {
    const { jobs } = this.state;

    const allInputParams = [{ name: '', type: 'string' }];

    const inputParams = CommonActions.getInputMetricColumnHeaders(
      allInputParams, [], () => {}, true, [],
    );

    const rows = [];

    jobs.forEach((job) => {
      rows.push(<div className="job-cell pop-up-cell i--icon-open-link" key={'job-pop-up'.concat(job.job_id)} />);
    });

    return (
      <div className="job-static-columns-container-popup">
        <div className="job-pop-up-no-title" />
        <div className="input-metric-header-row-container">
          <div className="input-metric-column-container-popup column-header">
            {inputParams}
          </div>
          <ScrollSyncPane group="vertical">
            <div className="input-metric-column-container-popup">
              {rows}
            </div>
          </ScrollSyncPane>
        </div>
      </div>
    );
  }
}
PopUpRows.propTypes = {
  jobs: PropTypes.array,
};

PopUpRows.defaultProps = {
  jobs: [],
};

export default PopUpRows;
