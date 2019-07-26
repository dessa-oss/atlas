import React from 'react';
import PropTypes from 'prop-types';
import SidebarSection from './SidebarSection';
import ArtifactViewer from './ArtifactViewer';
import ImageViewer from './ImageViewer';
import ArchiveList from './ArchiveList';

export default function JobSidebar(props) {
  if (props.job != null) {
    return (
      <div className="job-sidebar">
        <SidebarSection
          header="JOB DETAILS"
          content={ArtifactViewer({ jobId: props.job.job_id, content: ImageViewer() })}
        />
        <SidebarSection header="FILES" content={ArchiveList()} />
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
