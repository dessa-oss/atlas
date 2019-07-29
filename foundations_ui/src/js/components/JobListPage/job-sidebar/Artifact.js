import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import FileDownload from 'js-file-download';
import ArtifactList from './ArtifactList';

export default function Artifact(props) {
  const { artifact, onClick } = props;
  return (
    <li onClick={() => onClick(artifact)} onKeyDown={() => onClick(artifact)}>
      <p>{artifact.filename}</p>
      <DownloadButton className="download-button" uri={artifact.uri} filename={artifact.filename} />
    </li>
  );
}

Artifact.propTypes = {
  artifact: PropTypes.object,
  onClick: PropTypes.func,
};

const defaultFunc = () => <p>Artifact: Missing onClick event.</p>;
Artifact.defaultProps = {
  artifact: { msg: 'Artifact: Missing `filename` prop.' },
  onClick: defaultFunc,
};

// import ReactAudioPlayer from 'react-audio-player';


function DownloadButton(props) {
  const { uri, filename } = props;

  const getImage = async () => {
    const response = await axios.get(uri, { responseType: 'blob' });
    console.log(response);
    FileDownload(response.data, filename);
  };

  const getImageLocally = () => null;
  return (
    <button type="button" onClick={getImage}> Download File </button>
  );
}

DownloadButton.propTypes = {
  uri: PropTypes.string,
  filename: PropTypes.string,
};

DownloadButton.defaultProps = {
  uri: 'DownloadButton: Missing `uri` prop.',
  filename: 'DownloadButton: Missing `filename` prop.',
};
