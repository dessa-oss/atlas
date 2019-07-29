import React from 'react';
import ReactDOM from 'react-dom';
import ReactAudioPlayer from 'react-audio-player';

export default function AudioPlayer(props) {
  const { url } = props;
  
  return (
    <>
    <ReactAudioPlayer
      src={url}
      controls 
    />
    </>
  );
}
  