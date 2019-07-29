import React from 'react';
import PropTypes from 'prop-types';

export default function SidebarSection(props) {
  const { header, children } = props;
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <p className="sidebar-section-header-text text-white">{header}</p>
      </div>
      {children}
    </div>
  );
}

SidebarSection.propTypes = {
  header: PropTypes.string.isRequired,
  children: PropTypes.element.isRequired,
};
