import React from 'react';
import PropTypes from 'prop-types';

export default function ArchiveViewer(props) {
  return (
    <div className="artifact-viewer">
      <h2>Artifact Viewer</h2>
      {props.content}
      <p>Job: {props.jobId}</p>
    </div>
  );
}

ArchiveViewer.propTypes = {
  jobId: PropTypes.string,
  content: PropTypes.func,
};

ArchiveViewer.defaultProps = {
  jobId: 'JOB ID PROP MISSING',
  content: <p>ArchiveViewer: CONTENT PROP MISSING</p>,
};
