import React, { useState } from 'react';
import deviceStore from '../store/deviceStore';

const ChromecastDeviceComponent = () => {
  const [chromecastList, setChromecastList] = useState(deviceStore.chromecast);
  const handleChromecastChange = () => {
    setChromecastList(deviceStore.chromecast);
  };

  deviceStore.setCallback('chromecast', handleChromecastChange);
  const device = [];
  chromecastList.forEach((el) => {
    device.push(<p key={el.uuid}>{el.name}</p>);
  });
  return (
    <div>
      <h1>Device</h1>
      <div>
        {device}
      </div>
    </div>
  );
};

export default ChromecastDeviceComponent;
