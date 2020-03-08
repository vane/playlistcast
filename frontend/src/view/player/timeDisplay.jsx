import React, { useState, useEffect } from 'react';
import movieTimeFormat from 'formatter/movieTimeFormat';

const TimeDisplay = ({ currentTime, duration }) => {
  const [timeData, setTimeData] = useState([
    movieTimeFormat(Math.round(currentTime)),
    movieTimeFormat(Math.round(duration)),
    Math.round(currentTime),
  ]);

  useEffect(() => {
    const timer = setTimeout(() => {
      let current = Math.min(timeData[2] + 1, Math.floor(duration));
      if (Math.abs(current - currentTime) > 10) {
        current = Math.round(currentTime);
      }
      setTimeData([
        movieTimeFormat(current),
        movieTimeFormat(Math.round(duration)),
        current,
      ]);
    }, 1000);
    return () => clearTimeout(timer);
  });

  return (
    <p>
      <span>{timeData[0]}</span>
      <span>/</span>
      <span>{timeData[1]}</span>
    </p>
  );
};

export default TimeDisplay;
