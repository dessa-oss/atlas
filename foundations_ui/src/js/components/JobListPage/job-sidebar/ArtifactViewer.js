import React from 'react';
import PropTypes from 'prop-types';

export default function ArtifactViewer(props) {
  const { jobId, content } = props;
  return (
    <div className="artifact-viewer">
      <h2>Artifact Viewer</h2>
      <p>Job: {jobId}</p>
      {content}
    </div>
  );
}

ArtifactViewer.propTypes = {
  jobId: PropTypes.string,
  content: PropTypes.func,
};

ArtifactViewer.defaultProps = {
  jobId: 'JOB ID PROP MISSING',
  content: <p>ArchiveViewer: CONTENT PROP MISSING</p>,
};
