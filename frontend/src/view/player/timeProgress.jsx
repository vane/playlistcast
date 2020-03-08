import React, { useState, useEffect } from 'react';
import { Slider } from 'antd';
import { chromecastSeek } from 'service/chromecast';
import movieTimeFormat from 'formatter/movieTimeFormat';


const TimeProgress = ({
  uid,
  currentTime,
  duration,
  playerState,
}) => {
  const [time, setTime] = useState(Math.floor(currentTime));

  if (playerState === 'PLAYING') {
    useEffect(() => {
      const timer = setTimeout(() => {
        let current = Math.min(time + 1, Math.floor(duration));
        if (Math.abs(current - currentTime) > 10) {
          current = Math.round(currentTime);
        }
        setTime(current);
      }, 1000);
      return () => clearTimeout(timer);
    });
  } else {
    useEffect(() => {
    });
  }

  const handleSeek = (value) => {
    chromecastSeek(uid, value);
  };

  const handleChange = (value) => {
    setTime(value);
  };

  return (
    <Slider
      max={Math.floor(duration)}
      value={time}
      onChange={handleChange}
      onAfterChange={handleSeek}
      tipFormatter={movieTimeFormat}
    />
  );
};

export default TimeProgress;
