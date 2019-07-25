import React from 'react';
import PropTypes from 'prop-types';

export default function SidebarSection(props) {
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <p className="sidebar-section-header-text text-white">{props.header}</p>
      </div>
      {props.content}
    </div>
  );
}

SidebarSection.propTypes = {
  header: PropTypes.string,
  content: PropTypes.func,
};

SidebarSection.defaultProps = {
  header: 'HEADER PROP MISSING',
  content: <p>SidebarSection: CONTENT PROP MISSING</p>,
};
