import React from 'react';
import PropTypes from 'prop-types';
import SidebarSection from './SidebarSection';
import ArtifactViewer from './ArtifactViewer';
import ImageViewer from './ImageViewer';
import ArtifactList from './ArtifactList';

export default function JobSidebar(props) {
  const { job } = props;
  const handleArtifactClick = () => alert('You clicked and artifact');
  if (props.job != null) {
    return (
      <div className="job-sidebar">
        <SidebarSection
          header="JOB DETAILS"
          content={ArtifactViewer({ jobId: job.job_id, content: ImageViewer() })}
        />
        <SidebarSection
          header="FILES"
          content={ArtifactList({ artifacts: job.artifacts, handleClick: handleArtifactClick })}
        />
      </div>
    );
  }
  return null;
}

JobSidebar.propTypes = {
  job: PropTypes.object,
};

JobSidebar.defaultProps = {
  job: 'JobSidebar: No job prop.',
};
