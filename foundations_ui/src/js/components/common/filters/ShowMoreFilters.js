import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ShowMoreFilters extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hiddenBubbles: this.props.hiddenBubbles,
      removeFilter: this.props.removeFilterCallback,
    };
  }

  render() {
    const { hiddenBubbles } = this.state;

    const filterBubbles = [];
    hiddenBubbles.forEach((bubble) => {
      const key = bubble.id;
      const name = bubble.id.split(/-(.+)/)[0];
      const value = bubble.id.split(/-(.+)/)[1];
      filterBubbles.push(
        <div key={key} className="bubble inline-block">
          <p className="font-bold">
            {name}:<span> {value}</span>
          </p>
          <button
            onClick={() => { this.state.removeFilter({ column: name, value }); }}
            type="button"
            className="close-button"
          />
        </div>,
      );
    });
    return (
      <div className="show-more-filters-container elevation-1">
        {filterBubbles}
      </div>
    );
  }
}

ShowMoreFilters.propTypes = {
  hiddenBubbles: PropTypes.array,
  removeFilterCallback: PropTypes.func,
};

ShowMoreFilters.defaultProps = {
  hiddenBubbles: [],
  removeFilterCallback: () => {},
};

export default ShowMoreFilters;
