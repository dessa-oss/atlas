import React from 'react';
import PropTypes from 'prop-types';

export default function ArtifactViewer(props) {
  const { jobId, children } = props;
  return (
    <div className="artifact-viewer">
      <h2>Artifact Viewer</h2>
      <p>Job: {jobId}</p>
      {children}
    </div>
  );
}

ArtifactViewer.propTypes = {
  jobId: PropTypes.string.isRequired,
  children: PropTypes.func.isRequired,
};
