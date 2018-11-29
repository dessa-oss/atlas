import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ShowMoreFilters from '../common/filters/ShowMoreFilters';
import CommonActions from '../../actions/CommonActions';

const borderSize = 2; // 1px per side

class JobHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleFilters = this.toggleFilters.bind(this);
    this.state = {
      project: this.props.project,
      filters: this.props.filters,
      bubbleRefs: [],
      bubblesHidden: 0,
      isShowingMoreFilters: false,
    };
  }

  componentDidMount() {
    const { bubbleRefs } = this.state;
    const { clientWidth } = this.bubbleContainer;

    let curWidth = 0;
    let numHidden = 0;
    bubbleRefs.forEach((bubble) => {
      curWidth += CommonActions.addBorderToElementWidth(bubble, borderSize);
      if (CommonActions.elementsWidthLargerThanParent(curWidth, clientWidth)) {
        bubble.className += ' hidden';
        numHidden += 1;
      }
    });

    this.setState({ bubblesHidden: numHidden });
  }

  toggleFilters() {
    const { isShowingMoreFilters } = this.state;
    this.setState({ isShowingMoreFilters: !isShowingMoreFilters });
  }

  render() {
    const {
      project, filters, bubbleRefs, bubblesHidden, isShowingMoreFilters,
    } = this.state;

    const filterBubbles = [];
    filters.forEach((filter) => {
      filterBubbles.push(
        <div ref={(e) => { bubbleRefs.push(e); }} key={filter.column} className="bubble inline-block">
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

    let moreFilters = null;
    let filterButtonText = 'View Filters';
    if (isShowingMoreFilters) {
      moreFilters = <ShowMoreFilters filters={filters} bubblesHidden={bubblesHidden} />;
      filterButtonText = 'Hide Filters';
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
          <h2 className="font-bold">{project.name}</h2>
          <p>Data Source: Unknown</p>
          <p className="font-bold">
            Project owner: <span>{project.owner}</span>
          </p>
          <p className="font-bold">
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
              {filterButtonText}
            </button>
          </div>
        </div>
        {moreFilters}
      </div>
    );
  }
}

JobHeader.propTypes = {
  numProjects: PropTypes.number,
  project: PropTypes.object,
  filters: PropTypes.array,
  bubbleRefs: PropTypes.array,
  bubblesHidden: PropTypes.number,
  isShowingMoreFilters: PropTypes.bool,
};

JobHeader.defaultProps = {
  numProjects: 0,
  project: { owner: 'null', created_at: 'null', name: 'null' },
  filters: [],
  bubbleRefs: [],
  bubblesHidden: 0,
  isShowingMoreFilters: false,
};

export default JobHeader;
