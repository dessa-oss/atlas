import React from 'react';
import PropTypes from 'prop-types';
import Notes from './Notes';
import Readme from './Readme';
import JobOverviewGraph from './JobOverviewGraph';
import BaseActions from '../../actions/BaseActions';
import CommonActions from '../../actions/CommonActions';
import CommonHeader from '../common/CommonHeader';
import Header from './Header';
import TagContainer from './TagContainer';
import CommonFooter from '../common/CommonFooter';

class ProjectOverview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      projectName: this.props.match.params.projectName,
      metrics: '',
      allMetrics: [],
      graphData: [],
      timerId: -1,
      tags: [],
      jobIDs: [],
    };
    this.setMetric = this.setMetric.bind(this);
    this.onClickProjectOverview = this.onClickProjectOverview.bind(this);
    this.onClickJobDetails = this.onClickJobDetails.bind(this);
    this.onKeyDown = this.onKeyDown.bind(this);
  }

  async reload() {
    const { location } = this.props;
    if (location) {
      const { projectName } = this.props.match.params;
      await BaseActions.getFromStaging(`projects/${projectName}/job_listing`)
        .then(result => {
          if (result && result.jobs) {
            this.setState({
              tags: CommonActions.getTagsFromJob(result.jobs),
              jobIDs: result.jobs.map(job => job.job_id),
            });
          }
        });
    }

    const { projectName, metrics } = this.state;
    let URL = `projects/${projectName}/overview_metrics`;
    if (metrics) {
      URL = `${URL}?metric_name=`;
      metrics.forEach(m => {
        URL = `${URL}${m}|`;
      });
      URL = URL.substring(0, URL.length - 1);
    }

    const APIGraphData = await BaseActions.getFromStaging(URL);

    if (APIGraphData) {
      const correctGraphData = [];
      APIGraphData.metric_query.forEach(graph => {
        let addGraph = true;
        graph.values.forEach(value => {
          if (typeof value[1] !== 'number') {
            addGraph = false;
          }
        });

        if (addGraph === true) {
          correctGraphData.push(graph);
        }
      });

      const allMetrics = APIGraphData.all_metric_names;

      if (correctGraphData.length > 0) {
        this.setState({ graphData: correctGraphData, allMetrics: allMetrics });
      } else {
        this.setState({ graphData: [], allMetrics: [] });
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

  async setMetric(newMetrics) {
    await this.setState({ metrics: newMetrics });
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

    if (location && location.state && location.state.project && location.state.project !== {}) {
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
      metrics, graphData, allMetrics, tags, jobIDs,
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
                Experiment Details
              </h3>
            </div>
            <TagContainer tags={tags} />
          </div>
          <div className="dashboard-content-container row">
            <section className="chart-and-notes col-md-8">
              <JobOverviewGraph
                metrics={metrics}
                graphData={graphData}
                allMetrics={allMetrics}
                setMetric={this.setMetric}
                jobIDs={jobIDs}
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
