import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import FileDownload from 'js-file-download';

export default function Artifact(props) {
  const { artifact, onClick } = props;
  return (
    <li id={artifact.archive_key} onClick={() => onClick(artifact)} onKeyDown={() => onClick(artifact)}>
      <FileNameFormatter artifact={artifact} />
      <DownloadButton className="download-button" uri={artifact.uri} filename={artifact.filename} />
    </li>
  );
}

function FileNameFormatter(props) {
  const { artifact } = props;

  if (artifact.archive_key === artifact.filename) {
    return (
      <p>{artifact.filename}</p>
    );
  }
  return (
    <p>{artifact.archive_key}: {artifact.filename}</p>
  );
}

Artifact.propTypes = {
  artifact: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired,
};

FileNameFormatter.propTypes = {
  artifact: PropTypes.object.isRequired,
};

function DownloadButton(props) {
  const { uri, filename } = props;

  const getImage = async (evnt) => {
    evnt.preventDefault();
    window.location = uri;
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
