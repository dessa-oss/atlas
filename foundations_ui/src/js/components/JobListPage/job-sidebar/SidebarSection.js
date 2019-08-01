import React from 'react';
import PropTypes from 'prop-types';

function CloseButton(props) {
  const { enableCloseButton, onCloseClickHandler } = props;
  if (enableCloseButton) {
    return (
      <div className="sidebar-section-close-button-container">
        <button
          onClick={onCloseClickHandler}
          className="sidebar-section-close-button i--icon-close"
          type="button"
        />
      </div>
    );
  }
  return null;
}

export default function SidebarSection(props) {
  const { header, children, onCloseClickHandler } = props;
  const { enableCloseButton } = props;
  console.log({ enableCloseButton });
  return (
    <div className="sidebar-section">
      <div className="sidebar-section-header">
        <p className="sidebar-section-header-text text-white">{header}</p>
        <CloseButton enableCloseButton={enableCloseButton} onCloseClickHandler={onCloseClickHandler} />
      </div>
      {children}
    </div>
  );
}

SidebarSection.propTypes = {
  header: PropTypes.string.isRequired,
  children: PropTypes.element.isRequired,
  onCloseClickHandler: PropTypes.func.isRequired,
  enableCloseButton: PropTypes.bool.isRequired,
};

CloseButton.propTypes = {
  onCloseClickHandler: PropTypes.func.isRequired,
  enableCloseButton: PropTypes.bool.isRequired,
};
