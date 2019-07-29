import React from 'react';
import PropTypes from 'prop-types';
import Artifact from './Artifact';

export default function ArtifactList(props) {
  const { handleClick, artifacts } = props;
  console.log(artifacts);
  // const artifactsObj = {
  //   artifact1: {
  //     filename: 'archive1.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   artifact2: {
  //     filename: 'archive2.wav',
  //     location: '/some/path/to/file2/',
  //   },
  //   artifact3: {
  //     filename: 'archive3.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact4: {
  //     filename: 'archive4.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact5: {
  //     filename: 'archive5.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact6: {
  //     filename: 'archive6.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact7: {
  //     filename: 'archive7.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact8: {
  //     filename: 'archive8.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact9: {
  //     filename: 'archive9.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact10: {
  //     filename: 'archive10.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact11: {
  //     filename: 'archive11.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact12: {
  //     filename: 'archive12.xml',
  //     location: '/some/path/to/file3/',
  //   },
  //   artifact13: {
  //     filename: 'archive13.xml',
  //     location: '/some/path/to/file3/',
  //   },
  // };
  // const files = artifactsObj.map((artifact) => {
  //   console.log(artifact.filename);
  //   return artifact.filename;
  // });
  const artifactComps = artifacts.map((artifact) => {
    return <Artifact key={artifact.fname} filename={artifact.filename} uri={artifact.uri} onClick={handleClick} />;
  });

  return (
    <ul className="artifact-list">
      {artifactComps}
    </ul>
  );
}

ArtifactList.propTypes = {
  handleClick: PropTypes.func,
  artifacts: PropTypes.array,
};

const defaultClick = () => alert('ArtifactList: Missing `handleClick` prop.');
ArtifactList.defaultProps = {
  handleClick: defaultClick,
  artifacts: ['ArtifactList: Artifacts missing.'],
};
