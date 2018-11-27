import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      project: this.props.project,
      filters: this.props.filters,
      bubbleWidth: 0,
      bubbleRefs: [],
      bubblesHidden: 0,
    };
  }

  componentDidMount() {
    const { bubbleWidth, bubbleRefs } = this.state;
    const { clientWidth } = this.bubbleContainer;

    let curWidth = 0;
    let numHidden = 0;
    bubbleRefs.forEach((bubble) => {
      curWidth += bubble.clientWidth + 2; // 2 is for border
      if (curWidth > clientWidth) {
        bubble.className += ' hidden';
        numHidden += 1;
      }
    });

    this.setState({ bubblesHidden: numHidden });
  }

  render() {
    const {
      project, filters, bubbleRefs, bubblesHidden,
    } = this.state;

    const filterBubbles = [];
    filters.forEach((filter) => {
      filterBubbles.push(
        <div ref={(e) => { bubbleRefs.push(e); }} key={filter.column} className="bubble sort-bubble">
          <p className="font-bold">
            {filter.column}:<span> {filter.value}</span>
          </p>
          <button type="button" className="close-button" />
        </div>,
      );
    });

    let moreBubbles = null;
    if (bubblesHidden > 0) {
      moreBubbles = (
        <div className="bubble more-bubble">
          <p className="font-bold text-blue text-upper">
          + {bubblesHidden} More
          </p>
        </div>
      );
    }

    return (
      <div className="job-header-container">
        <div className="job-header-logo-container">
          <div className="i--icon-logo" />
          <h2 className="font-bold">Foundations</h2>
        </div>
        <div className="job-header-info-container">
          <div>
            <div className="half-width inline-block">
              <h1 className="blue-border-bottom font-bold">Job List</h1>
            </div>
          </div>
        </div>

        <div className="job-summary-info-container">
          <h2 className="project-summary-name-text font-bold">{ project.name }</h2>
          <p className="project-summary-source-text">Data Source: Unknown</p>
          <p className="project-summary-owner-text font-bold">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="project-summary-created-at-text font-bold">
            Created at: <span>{project.created_at}</span>
          </p>
        </div>
        <div className="job-header-sorting-container">
          <button
            type="button"
            onClick={this.onClearFilters}
            className="b--mat b--affirmative text-upper"
          >
            Clear Filters
          </button>
          <div>
            <div ref={(e) => { this.bubbleContainer = e; }}>
              {filterBubbles}
            </div>
            {moreBubbles}
          </div>
          <div>
            <button
              type="button"
              onClick={this.toggleFilters}
              className="b--mat b--affirmative text-upper"
            >
              View Filters
            </button>
          </div>
        </div>
      </div>
    );
  }
}

JobHeader.propTypes = {
  numProjects: PropTypes.number,
  project: PropTypes.object,
  filters: PropTypes.array,
  bubbleWidth: PropTypes.number,
  bubbleRefs: PropTypes.array,
  bubblesHidden: PropTypes.number,
};

JobHeader.defaultProps = {
  numProjects: 0,
  project: { owner: 'null', created_at: 'null', name: 'null' },
  filters: [],
  bubbleWidth: 0,
  bubbleRefs: [],
  bubblesHidden: 0,
};

export default JobHeader;
