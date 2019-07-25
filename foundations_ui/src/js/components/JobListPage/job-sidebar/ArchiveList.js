import React from 'react';
import PropTypes from 'prop-types';
import ListItem from './ListItem';

export default function ArchiveList(props) {
  const artifacts = {
    artifact1: {
      filename: 'archive1.jpg',
      location: '/some/path/to/file1/',
    },
    artifact2: {
      filename: 'archive2.wav',
      location: '/some/path/to/file2/',
    },
    artifact3: {
      filename: 'archive3.xml',
      location: '/some/path/to/file3/',
    },
    artifact4: {
      filename: 'archive4.xml',
      location: '/some/path/to/file3/',
    },
    artifact5: {
      filename: 'archive5.xml',
      location: '/some/path/to/file3/',
    },
    artifact6: {
      filename: 'archive6.xml',
      location: '/some/path/to/file3/',
    },
    artifact7: {
      filename: 'archive7.xml',
      location: '/some/path/to/file3/',
    },
    artifact8: {
      filename: 'archive8.xml',
      location: '/some/path/to/file3/',
    },
    artifact9: {
      filename: 'archive9.xml',
      location: '/some/path/to/file3/',
    },
    artifact10: {
      filename: 'archive10.xml',
      location: '/some/path/to/file3/',
    },
  };
  const files = Object.values(artifacts).map((artifact) => {
    console.log(artifact.filename);
    return artifact.filename;
  });
  const listItems = files.map(fname => <ListItem key={fname} filename={fname} />);
  return (
    <ul className="artifact-list">
      {listItems}
    </ul>
  );
}
