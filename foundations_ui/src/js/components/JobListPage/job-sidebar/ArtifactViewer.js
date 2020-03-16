import React from 'react';
import PropTypes from 'prop-types';

export default function ArtifactViewer(props) {
  const { jobId, children } = props;
  return (
    <div className="artifact-viewer">
      <p className="job">Job ID: {jobId}</p>
      {children}
    </div>
  );
}

ArtifactViewer.propTypes = {
  jobId: PropTypes.string.isRequired,
  children: PropTypes.func.isRequired,
};
