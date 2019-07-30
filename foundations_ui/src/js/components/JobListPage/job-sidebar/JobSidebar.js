import React, { useState } from 'react';
import PropTypes from 'prop-types';
import SidebarSection from './SidebarSection';
import ArtifactViewer from './ArtifactViewer';
import ImageViewer from './ImageViewer';
import ArtifactList from './ArtifactList';
import AudioPlayer from './AudioPlayer';

export default function JobSidebar(props) {
  const { job } = props;
  if (job.job_id !== null) {
    if (job.artifacts && job.artifacts.length > 0) {
      const [selectedArtifact, setArtifact] = useState(job.artifacts[0]);
      const handleArtifactClick = artifact => setArtifact(artifact);

      const [currentJob, setJob] = useState(job);
      if (job !== currentJob) {
        setArtifact(job.artifacts[0]);
        setJob(job);
      }

      const selectViewer = (artifact) => {
        switch (artifact.artifact_type) {
          case 'image':
            return <ImageViewer image={artifact.uri} />;
          case 'audio':
            return <AudioPlayer url={artifact.uri} />;
          default:
            return <p className="media">This filetype is not viewable.</p>;
        }
      };

      return (
        <div className="job-sidebar">
          <SidebarSection header="JOB DETAILS">
            <ArtifactViewer jobId={currentJob.job_id}>
              {selectViewer(selectedArtifact)}
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
        <SidebarSection header="JOB DETAILS">
          <ArtifactViewer jobId={job.job_id}>
            <p>No artifacts for this job</p>
          </ArtifactViewer>
        </SidebarSection>
      </div>
    );
  }
  return null;
}

JobSidebar.propTypes = {
  job: PropTypes.object.isRequired,
};
