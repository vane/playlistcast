import React from 'react';
import chromecastDeviceAll from '../service/device';
import deviceStore from '../store/deviceStore';

const ChromecastDeviceComponent = () => {
  chromecastDeviceAll(deviceStore);
  return (
    <div>
      <h1>Device</h1>
    </div>
  );
};

export default ChromecastDeviceComponent;
