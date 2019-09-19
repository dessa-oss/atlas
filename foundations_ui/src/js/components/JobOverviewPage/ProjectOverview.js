import React from 'react';
import PropTypes from 'prop-types';
import Notes from './Notes';
import Readme from './Readme';
import JobOverviewGraph from './JobOverviewGraph';
import BaseActions from '../../actions/BaseActions';
import CommonHeader from '../common/CommonHeader';
import Header from './Header';
import TagContainer from './TagContainer';
import CommonFooter from '../common/CommonFooter';

class ProjectOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.match.params.projectName,
      metric: '',
      allMetrics: [],
      graphData: [],
      timerId: -1,
      tags: [],
    };
    this.setMetric = this.setMetric.bind(this);
    this.onClickProjectOverview = this.onClickProjectOverview.bind(this);
    this.onClickJobDetails = this.onClickJobDetails.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  async reload() {
    const { location } = this.props;
    if (!location.state || !location.state.project || location.state.project === {}) {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.getFromStaging('projects');
      const selectedProject = fetchedProjects.filter(item => item.name === projectName);
      this.setState({
        tags: selectedProject.tags,
      });
    }

    const { projectName, metric } = this.state;
    let URL = `projects/${projectName}/overview_metrics`;
    if (metric) {
      URL = `${URL}?metric_name=${metric}`;
    }

    const APIGraphData = await BaseActions.getFromStaging(URL);

    if (APIGraphData.length > 0) {
      let correctGraphData = [];
      APIGraphData.forEach((graph) => {
        let addGraph = true;
        graph.values.forEach((value) => {
          if (typeof value[1] !== 'number') {
            addGraph = false;
          }
        });

        if (addGraph === true) {
          correctGraphData.push(graph);
        }
      });

      const allMetrics = correctGraphData.map((graphMetric) => {
        return graphMetric.metric_name;
      });

      if (correctGraphData.length > 0) {
        this.setState({ graphData: correctGraphData[0].values, metric: correctGraphData[0].metric_name, allMetrics });
      } else {
        this.setState({ graphData: [], metric: '', allMetrics: [] });
      }
    }
  }

  componentDidMount() {
    this.reload();
    const value = setInterval(() => {
      this.reload();
    }, 20000);
    this.setState({
      timerId: value,
    });
  }

  componentWillUnmount() {
    const { timerId } = this.state;
    clearInterval(timerId);
  }

  async setMetric(newMetric) {
    await this.setState({ metric: newMetric });
    this.reload();
  }

  async onClickProjectOverview() {
    const { history, location } = this.props;
    let selectedProject = {};

    if (location.state.project && location.state.project !== {}) {
      selectedProject = location.state.project;
    } else {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.getFromStaging('projects');
      selectedProject = fetchedProjects.filter(item => item.name === projectName);
    }
    history.push(
      `/projects/${selectedProject.name}/overview`,
      {
        project: selectedProject,
      },
    );
  }

  async onClickJobDetails() {
    const { history, location } = this.props;
    let selectedProject = {};

    if (location.state.project && location.state.project !== {}) {
      selectedProject = location.state.project;
    } else {
      const { projectName } = this.props.match.params;
      const fetchedProjects = await BaseActions.getFromStaging('projects');
      selectedProject = fetchedProjects.filter(item => item.name === projectName);
    }
    history.push(
      `/projects/${selectedProject.name}/job_listing`,
      {
        project: selectedProject,
      },
    );
  }

  onKeyDown() {}

  render() {
    const {
      metric, graphData, allMetrics, tags,
    } = this.state;

    return (
      <div>
        <CommonHeader {...this.props} />
        <div className="job-overview-container">
          <Header {...this.props} />
          <div className="job-overview-tabs-tags-container">
            <div>
              <h3
                className="active"
                onClick={this.onClickProjectOverview}
                onKeyDown={this.onKeyDown}
              >
                Project Overview
              </h3>
              <h3
                onClick={this.onClickJobDetails}
                onKeyDown={this.onKeyDown}
              >
                Job Details
              </h3>
            </div>
            <TagContainer tags={tags} />
          </div>
          <div className="dashboard-content-container row">
            <section className="chart-and-notes col-md-8">
              <JobOverviewGraph
                metric={metric}
                graphData={graphData}
                allMetrics={allMetrics}
                setMetric={this.setMetric}
              />
              <Readme {...this.props} />
            </section>
            <Notes {...this.props} />
          </div>
        </div>
        <CommonFooter />
      </div>
    );
  }
}

ProjectOverview.propTypes = {
  history: PropTypes.object,
  match: PropTypes.object,
  location: PropTypes.object,
};

ProjectOverview.defaultProps = {
  history: {},
  match: { params: {} },
  location: { state: {} },
};

export default ProjectOverview;
