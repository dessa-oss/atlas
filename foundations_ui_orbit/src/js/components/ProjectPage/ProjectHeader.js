import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ProjectHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numProjects: this.props.numProjects,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ numProjects: nextProps.numProjects });
  }

  render() {
    const { numProjects } = this.state;

    return (
      <div className="project-header-container">
        <div className="project-header-logo-container">
          <div className="i--icon-logo" />
          <h2 className="font-bold">Foundations</h2>
        </div>
        <div className="project-header-info-container">
          <div className="project-header-total-projects-container">
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">Projects</h1>
            </div>
            <div className="half-width inline-block text-right">
              <h2 className="blue-border-bottom font-bold">
                Total Projects: <span>{numProjects}</span>
              </h2>
            </div>
          </div>
          <div className="project-header-sort-filter-container" />
        </div>
      </div>
    );
  }
}

ProjectHeader.propTypes = {
  numProjects: PropTypes.number,
};

ProjectHeader.defaultProps = {
  numProjects: 0,
};

export default ProjectHeader;
