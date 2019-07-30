import React from 'react';
import PropTypes from 'prop-types';
import Artifact from './Artifact';

export default function ArtifactList(props) {
  const { handleClick, artifacts } = props;
  console.log(artifacts);
  // const artifactsObj = [
  //   {
  //     filename: 'archive1.jpg',
  //     location: '/some/path/to/file1/',
  //     // uri: '1',
  //   },
  //   {
  //     filename: 'archive3.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   {
  //     filename: 'archive4.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   {
  //     filename: 'archive5.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   {
  //     filename: 'archive6.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   {
  //     filename: 'archive7.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  //   {
  //     filename: 'archive8.jpg',
  //     location: '/some/path/to/file1/',
  //   },
  // ];
  // const files = artifactsObj.map((artifact) => {
  //   console.log(artifact.filename);
  //   return artifact.filename;
  // });
  // const artifactList = [{
  //   filename: 'test1',
  //   uri: 'https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
  // }, {
  //   filename: 'test2',
  //   uri: 'https://images.pexels.com/photos/853168/pexels-photo-853168.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
  // }];

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
  handleClick: PropTypes.func,
  artifacts: PropTypes.array,
};

const defaultClick = () => alert('ArtifactList: Missing `handleClick` prop.');
ArtifactList.defaultProps = {
  handleClick: defaultClick,
  artifacts: ['ArtifactList: Artifacts missing.'],
};
