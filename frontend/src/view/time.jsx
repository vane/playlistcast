import moment from 'moment';
import React, { useState, useEffect } from 'react';
import timeStore from '../store/timeStore';

const timeStyle = {
  position: 'absolute',
  top: '10px',
  right: '10px',
};

const TimeComponent = () => {
  const [time, setTime] = useState(timeStore.time);

  const updateTime = () => {
    setTime(timeStore.time);
  };

  useEffect(() => {
    timeStore.setCallback('updateTime', updateTime);
    return () => {
      timeStore.delCallback('updateTime', updateTime);
    };
  });

  return (<div style={timeStyle}>{`${moment(time).format('YYYY-MM-DD HH:mm:ss')}`}</div>);
};

export default TimeComponent;
