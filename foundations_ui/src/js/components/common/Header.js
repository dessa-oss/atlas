import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ProjectHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numProjects: this.props.numProjects,
      pageTitle: this.props.pageTitle,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ numProjects: nextProps.numProjects });
  }

  render() {
    const { numProjects, pageTitle } = this.state;

    let projectCount;

    if (pageTitle === 'Projects') {
      projectCount = (
        <div className="half-width inline-block text-right">
          <h2 className="blue-border-bottom font-bold">
              Total Projects: <span>{numProjects}</span>
          </h2>
        </div>
      );
    }


    return (
      <div className="project-header-container">
        <div className="project-header-info-container">
          <div className="project-header-total-projects-container">
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">{pageTitle}</h1>
            </div>
            {projectCount}
            <div className="project-header-sort-filter-container" />
          </div>
        </div>
      </div>
    );
  }
}

ProjectHeader.propTypes = {
  numProjects: PropTypes.number,
  pageTitle: PropTypes.string,
};

ProjectHeader.defaultProps = {
  numProjects: 0,
  pageTitle: 'Projects',
};

export default ProjectHeader;
