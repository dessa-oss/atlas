import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import FileDownload from 'js-file-download';

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
  artifact: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired,
};

function DownloadButton(props) {
  const { uri, filename } = props;

  const getImage = async () => {
    const response = await axios.get(uri, { responseType: 'blob' });
    FileDownload(response.data, filename);
  };

  return (
    <button type="button" onClick={getImage}>
      <div className="i--icon-download" />
    </button>
  );
}

DownloadButton.propTypes = {
  uri: PropTypes.string.isRequired,
  filename: PropTypes.string.isRequired,
};
