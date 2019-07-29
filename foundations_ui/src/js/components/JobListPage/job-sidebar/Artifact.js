import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import FileDownload from 'js-file-download';

export default function Artifact(props) {
  const { filename, uri } = props;
  return (
    <li>
      <p>{filename}</p>
      <DownloadButton className="download-button" uri={uri} />
    </li>
  );
}

Artifact.propTypes = {
  filename: PropTypes.string,
  uri: PropTypes.string,
};

Artifact.defaultProps = {
  filename: 'Artifact: Missing `filename` prop.',
  uri: 'Artifact: Missing `uri` prop.',
};

// import ReactAudioPlayer from 'react-audio-player';


function DownloadButton(props) {
  const { uri } = props;
  const getImage = async () => {
    const response = await axios.get(uri, { responseType: 'blob' });
    console.log(response);
    FileDownload(response.data, 'test-data.tgz');
  };

  // const getImageLocally
  return (
    <button type="button" onClick={getImage}> Download File </button>
  );
}

DownloadButton.propTypes = {
  uri: PropTypes.string,
};

DownloadButton.defaultProps = {
  uri: 'DownloadButton: Missing `uri` prop.',
};
