import React from 'react';
import Notes from './Notes';
import Readme from './Readme';

class ProjectOverview extends React.Component {
  render() {
    return (
      <div className="dashboard-content-container row">
        <section className="chart-and-notes col-md-8">
          <div className="chart section-container">
            <h3>Recent Jobs</h3>
            <select>
              <option selected="selected">
                Metrics
              </option>
            </select>
            <select>
              <option selected="selected">
                Sort by
              </option>
            </select>
          </div>
          <Notes />
        </section>
        <Readme />
      </div>
    );
  }
}

export default ProjectOverview;
