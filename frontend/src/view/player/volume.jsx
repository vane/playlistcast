import React, { useEffect } from 'react';
import { Col, Slider } from 'antd';
import { chromecastVolumeChange } from 'service/chromecast';

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
    <Col span={4}>
      <Slider defaultValue={volumeLevel * 100} onChange={handleVolumeChange} />
    </Col>
  );
};

export default VolumeComponent;
