import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ShowMoreFilters extends Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: this.props.filters,
      bubblesHidden: this.props.bubblesHidden,
    };
  }

  render() {
    const { filters, bubblesHidden } = this.state;

    const filterBubbles = [];
    for (let i = 1; i <= bubblesHidden; i += 1) {
      const index = filters.length - i;
      filterBubbles.push(
        <div key={filters[index].column} className="bubble inline-block">
          <p className="font-bold">
            {filters[index].column}:<span> {filters[index].value}</span>
          </p>
          <button type="button" className="close-button" />
        </div>,
      );
    }

    return (
      <div className="show-more-filters-container elevation-1">
        {filterBubbles}
      </div>
    );
  }
}

ShowMoreFilters.propTypes = {
  filters: PropTypes.array,
  bubblesHidden: PropTypes.number,
};

ShowMoreFilters.defaultProps = {
  filters: [],
  bubblesHidden: 0,
};

export default ShowMoreFilters;
