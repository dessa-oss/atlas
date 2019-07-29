import React from 'react';
import PropTypes from 'prop-types';
import ReactAudioPlayer from 'react-audio-player';

export default function AudioPlayer(props) {
  const { url } = props;
  return <ReactAudioPlayer src={url} controls />;
}

AudioPlayer.propTypes = {
  url: PropTypes.string,
};

AudioPlayer.defaultProps = {
  url: 'AudioPlayer: No uri prop.',
};
