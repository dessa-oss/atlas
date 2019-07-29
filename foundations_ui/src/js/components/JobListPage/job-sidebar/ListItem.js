import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import FileDownload from 'js-file-download';

export default function ListItem(props) {
  return (
    <li>
      <p>{props.filename}</p>
      <DownloadButton />
    </li>
  );
}

ListItem.propTypes = {
  filename: PropTypes.string,
};

ListItem.defaultProps = {
  filename: 'ListItem: Missing `filename` prop.',
};

// import ReactAudioPlayer from 'react-audio-player';


class DownloadButton extends React.Component {
  getImage() {
    return axios.get(
      'http://192.168.128.41:31335/24da0eb8-7e54-4624-af42-68ec4c67eaf7/job_source/24da0eb8-7e54-4624-af42-68ec4c67eaf7.tgz', {
        responseType: 'blob',
      },
    ).then((response) => {
      FileDownload(response.data, 'test-data.tgz');
    });
  }

  render() {
    return (
      <button type="button" onClick={this.getImage}> Download File </button>
    );
  }
}
