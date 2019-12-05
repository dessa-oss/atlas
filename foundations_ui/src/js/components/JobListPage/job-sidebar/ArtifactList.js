import React from 'react';
import PropTypes from 'prop-types';
import Artifact from './Artifact';

export default function ArtifactList(props) {
  const { handleClick, artifacts } = props;

  const artifactComps = (artifacts || []).map((artifact) => {
    return <Artifact key={artifact.id} artifact={artifact} onClick={handleClick} />;
  });

  return (
    <ul className="artifact-list">
      {artifactComps}
    </ul>
  );
}

ArtifactList.propTypes = {
  handleClick: PropTypes.func.isRequired,
  artifacts: PropTypes.array.isRequired,
};
