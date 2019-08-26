import React from 'react';
import PropTypes from 'prop-types';
import HoverCell from '../JobListPage/cells/HoverCell';

const maxLength = 6;

class TagContainer extends React.Component {
  constructor(props) {
    super(props);
    this.isTagContentOverMaxLength = this.isTagContentOverMaxLength.bind(this);
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseLeave = this.onMouseLeave.bind(this);
    this.state = {
      tags: this.props.tags,
      showExpandedTags: false,
    };
  }

  isTagContentOverMaxLength() {
    const { tags } = this.state;
    return tags.length >= maxLength;
  }

  onMouseEnter() {
    this.setState({ showExpandedTags: true });
  }

  onMouseLeave() {
    this.setState({ showExpandedTags: false });
  }

  render() {
    const { tags, showExpandedTags } = this.state;

    const tagSpans = [];
    let expandedTagSpans = [];
    let index = 0;
    let hover = null;
    tags.forEach((tag) => {
      if (index === maxLength) {
        expandedTagSpans = Array.from(tagSpans);
        tagSpans.push(<span
          className="view-all-tags"
          key="view-all-tags"
          onMouseEnter={this.onMouseEnter}
          onFocus={this.onMouseOver}
        >View all tags</span>);
        expandedTagSpans.push(<span key={'tag-'.concat(tag)}>{tag}</span>);
      } else if (index < maxLength) {
        tagSpans.push(<span key={'tag-'.concat(tag)}>{tag}</span>);
      } else {
        expandedTagSpans.push(<span key={'tag-'.concat(tag)}>{tag}</span>);
      }
      index += 1;
    });

    if (showExpandedTags && this.isTagContentOverMaxLength()) {
      hover = <HoverCell onMouseLeave={this.onMouseLeave} textToRender={expandedTagSpans} />;
    }

    return (
      <div className="project-summary-tags-container">
        <p>tags</p>
        <div onMouseLeave={this.onMouseLeave} onBlur={this.onMouseOut}>
          {tagSpans}
          {hover}
        </div>
      </div>
    );
  }
}

TagContainer.propTypes = {
  tags: PropTypes.object,

};

TagContainer.defaultProps = {
  tags: [],
};

export default TagContainer;
