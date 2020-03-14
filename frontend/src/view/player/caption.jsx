import React, { useState } from 'react';
import { Button } from 'antd';
import { chromecastSubtitleDisable, chromecastSubtitleEnable } from 'service/chromecast';

const CaptionComponent = ({ uid, trackList }) => {
  console.log(uid, trackList);
  const [subtitles, setSubtitles] = useState(trackList);
  const handleSubtitleChange = (trackId) => {
    console.log('subtitle', uid, trackId);
    if (trackId < 0) {
      chromecastSubtitleDisable(uid);
    } else {
      chromecastSubtitleEnable(uid, trackId);
    }
  };
  const tracks = [];
  if (subtitles) {
    subtitles.forEach((track) => {
      const c = (
        <Button
          key={track.trackId}
          onClick={() => handleSubtitleChange(track.trackId)}
        >
          { track.name || track.language }
        </Button>
      );
      tracks.push(c);
    });
    tracks.push(<Button key="clear_caption" onClick={() => handleSubtitleChange(-1)}>clear</Button>);
  } else {
    setSubtitles([]);
  }
  return (
    <div>
      <h1>Captions</h1>
      <div>{tracks}</div>
    </div>
  );
};

export default CaptionComponent;
