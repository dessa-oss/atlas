import React, { useState } from 'react';
import PropTypes from 'prop-types';
import SidebarSection from './SidebarSection';
import ArtifactViewer from './ArtifactViewer';
import ImageViewer from './ImageViewer';
import ArtifactList from './ArtifactList';

export default function JobSidebar(props) {
  const { job } = props;
  if (job !== null) {
    if (job.artifacts && job.artifacts.length > 0) {
      // job.artifacts[0].uri = 'https://cdn.pixabay.com/photo/2018/01/04/19/43/love-3061483__340.jpg';
      // if (job.artifacts.length > 0) { }
      const [selectedArtifact, setArtifact] = useState(job.artifacts[0]);
      const handleArtifactClick = artifact => setArtifact(artifact);
      return (
        <div className="job-sidebar">
          <SidebarSection header="JOB DETAILS">
            <ArtifactViewer jobId={job.job_id}>
              <ImageViewer image={selectedArtifact.uri} />
            </ArtifactViewer>
          </SidebarSection>
          <SidebarSection header="FILES">
            <ArtifactList artifacts={job.artifacts} handleClick={handleArtifactClick} />
          </SidebarSection>
        </div>
      );
    }
    return (
      <div className="job-sidebar">
        <SidebarSection
          header="JOB DETAILS"
          content={ArtifactViewer({
            jobId: job.job_id,
            content: 'No artifact for this job',
          })
          }
        />
      </div>
    );
  }
  return null;
}

JobSidebar.propTypes = {
  job: PropTypes.object.isRequired,
};
