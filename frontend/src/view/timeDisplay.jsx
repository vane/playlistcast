import React, { useState, useEffect } from 'react';
import movieTimeFormat from '../formatter/movieTimeFormat';

const TimeDisplay = ({ currentTime, duration }) => {
  const [timeData, setTimeData] = useState(['', '', Math.round(currentTime)]);
  useEffect(() => {
    const timer = setTimeout(() => {
      const current = timeData[2] + 1;
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
