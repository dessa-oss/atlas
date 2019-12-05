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

  componentWillReceiveProps(nextProps) {
    if (nextProps.tag !== this.props.tag) {
      this.setState({
        tags: nextProps.tag,
        rowNumber: nextProps.rowNumber,
        isError: nextProps.isError,
      });
    }
  }

  render() {
    const { tags, isError, rowNumber } = this.state;

    const pClass = isError
      ? `job-cell tag-cell error row-${rowNumber}`
      : `job-cell tag-cell row-${rowNumber}`;

    const tagList = [];
    const someTagKeys = Object.keys(tags);

    someTagKeys.map((keyName) => {
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
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
  tag: PropTypes.object,
};

TagsCell.defaultProps = {
  isError: false,
  rowNumber: 0,
  tag: {},
};

export default TagsCell;
