import React from 'react';
import PropTypes from 'prop-types';
import Notes from './Notes';
import Readme from './Readme';
import JobOverviewGraph from './JobOverviewGraph';
import BaseActions from '../../actions/BaseActions';

class ProjectOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.history.location.state.project.name,
      metric: '',
      graphData: [],
    };

    this.getGraphData = this.getGraphData.bind(this);
  }

  componentDidMount() {
    this.getGraphData();
  }

  async getGraphData() {
    const { projectName } = this.state;
    const URL = '/projects/'.concat(projectName).concat('/graph');
    const APIGraphData = await BaseActions.getFromApiary(URL);
    this.setState({ graphData: APIGraphData.data, metric: APIGraphData.metric });
  }

  render() {
    const {
      metric, graphData,
    } = this.state;

    return (
      <div className="dashboard-content-container row">
        <section className="chart-and-notes col-md-8">
          <JobOverviewGraph metric={metric} graphData={graphData} />
          <Readme {...this.props} />
        </section>
        <Notes />
      </div>
    );
  }
}

ProjectOverview.propTypes = {
  history: PropTypes.object,
};

ProjectOverview.defaultProps = {
  history: {},
};

export default ProjectOverview;
