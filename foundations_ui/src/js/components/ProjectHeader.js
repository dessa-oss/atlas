import React, { Component } from 'react';

class ProjectHeader extends Component {
  render() {
    return (
      <div className="project-header-container">
        <div className="project-header-logo-container">
          <div className="i--icon-logo project-header-logo" />
          <p className="project-header-logo-text">Foundations</p>
        </div>
        <div className="project-header-info-container">
          <div className="project-header-total-projects-container">
            <div className="project-header-projects-container">
              <p className="project-header-projects-text blue-border-bottom">Projects</p>
            </div>
            <div className="project-header-total-projects-container">
              <p className="project-header-total-projects-text blue-border-bottom">Total Projects:</p>
              <p className="project-header-total-projects-number-text blue-border-bottom font-regular">37</p>
            </div>
          </div>
          <div className="project-header-sort-filter-container" />
        </div>
      </div>
    );
  }
}

export default ProjectHeader;
