import React, { useState } from 'react';
import PropTypes from 'prop-types';
import SidebarSection from './SidebarSection';
import ArtifactViewer from './ArtifactViewer';
import ImageViewer from './ImageViewer';
import ArtifactList from './ArtifactList';

export default function JobSidebar(props) {
  const { job } = props;
  if (job != null) {
    // job.artifacts[0].uri = 'https://cdn.pixabay.com/photo/2018/01/04/19/43/love-3061483__340.jpg';
    const [selectedArtifact, setArtifact] = useState(job.artifacts[0]);
    const handleArtifactClick = artifact => setArtifact(artifact);
    console.log(selectedArtifact);
    return (
      <div className="job-sidebar">
        <SidebarSection
          header="JOB DETAILS"
          content={ArtifactViewer({
            jobId: job.job_id,
            content: ImageViewer({ image: selectedArtifact.uri }),
          })
        }
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
