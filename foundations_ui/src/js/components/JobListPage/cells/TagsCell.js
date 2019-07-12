import React, { Component } from 'react';
import PropTypes from 'prop-types';

class TagsCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
      tags: this.props.tag,
    };
  }

  render() {
    const { tags, isError, rowNumber } = this.state;

    const pClass = isError
      ? `job-cell tag-cell error row-${rowNumber}`
      : `job-cell tag-cell row-${rowNumber}`;

    const tagList = [];
    const someTagKeys = Object.keys(tags);

    someTagKeys.map((keyName) => {
      // console.log('tags.key', tags[keyName]);
      tagList.push(<div className="tagBlock">{keyName}:{tags[keyName]}</div>);
    });

    return (
      <div className={pClass}>
        <div className="tagWrapper">
          {tagList}
        </div>
      </div>
    );
  }
}

TagsCell.propTypes = {
  tag: PropTypes.object,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

TagsCell.defaultProps = {
  tag: {},
  isError: false,
  rowNumber: 0,
};

export default TagsCell;
