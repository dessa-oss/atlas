import React, { Component } from 'react';
import PropTypes from 'prop-types';

class ShowMoreFilters extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hiddenBubbles: this.props.hiddenBubbles,
    };
  }

  render() {
    const { hiddenBubbles } = this.state;

    const filterBubbles = [];
    hiddenBubbles.forEach((bubble) => {
      const key = bubble.id;
      const splitId = bubble.id.split('-');
      filterBubbles.push(
        <div key={key} className="bubble inline-block">
          <p className="font-bold">
            {splitId[0]}:<span> {splitId[1]}</span>
          </p>
          <button type="button" className="close-button" />
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
};

ShowMoreFilters.defaultProps = {
  hiddenBubbles: [],
};

export default ShowMoreFilters;
