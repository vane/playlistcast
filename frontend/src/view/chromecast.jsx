import React, { useState } from 'react';
import chromecastStore from '../store/chromecastStore';

const ChromecastDeviceComponent = () => {
  const [chromecastList, setChromecastList] = useState(chromecastStore.chromecast);
  const handleChromecastChange = () => {
    setChromecastList(chromecastStore.chromecast);
  };

  chromecastStore.setCallback('chromecast', handleChromecastChange);
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
