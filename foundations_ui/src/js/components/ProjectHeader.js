import React, { Component } from 'react';

class ProjectHeader extends Component {
  render() {
    return (
      <div className="project-header-container">
        <div className="project-header-logo-container">
          <div className="i--icon-logo" />
          <h2>Foundations</h2>
        </div>
        <div className="project-header-info-container">
          <div className="project-header-total-projects-container">
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom">Projects</h1>
            </div>
            <div className="half-width inline-block text-right">
              <h2 className="blue-border-bottom">
                Total Projects: <span className="font-regular">37</span>
              </h2>
            </div>
          </div>
          <div className="project-header-sort-filter-container" />
        </div>
      </div>
    );
  }
}

export default ProjectHeader;
