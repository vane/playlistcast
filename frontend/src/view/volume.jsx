import React, { useEffect } from 'react';
import { Slider } from 'antd';
import { chromecastVolumeChange } from '../service/chromecast';

const VolumeComponent = ({ uid, volumeLevel }) => {
  let id = null;
  const handleVolumeChange = (value) => {
    if (id) clearTimeout(id);
    id = setTimeout(() => {
      chromecastVolumeChange(uid, value * 0.01);
    }, 500);
  };

  useEffect(() => () => clearTimeout(id));

  return (
    <Slider defaultValue={volumeLevel * 100} onChange={handleVolumeChange} />
  );
};

export default VolumeComponent;
