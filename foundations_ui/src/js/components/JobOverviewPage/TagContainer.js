import React from 'react';
import PropTypes from 'prop-types';

function TagContainer(props) {
  const { tags } = props;

  return (
    <div className="project-summary-tags-container" data-class="project-page-tags">
      <p>tags</p>
      <div className="project-summary-tags-container-inner">
        {tags.map(tag => <span key={'tag-'.concat(tag)}>{tag}</span>)}
      </div>
    </div>
  );
}

TagContainer.propTypes = {
  tags: PropTypes.object,

};

TagContainer.defaultProps = {
  tags: [],
};

export default TagContainer;
