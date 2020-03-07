import React, { useState } from 'react';
import { Card } from 'antd';
import chromecastStore from '../store/chromecastStore';
import TimeDisplay from './timeDisplay';


const ChromecastDeviceComponent = () => {
  const [chromecastList, setChromecastList] = useState(chromecastStore.chromecast);
  const handleChromecastChange = () => {
    setChromecastList(chromecastStore.chromecast);
  };

  chromecastStore.setCallback('chromecast', handleChromecastChange);
  const device = [];
  chromecastList.forEach((el) => {
    device.push(<ChromecastDevice key={el.uuid} device={el} />);
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

const ChromecastDevice = ({ device }) => {
  const mc = device.mediaController;
  const [status, setStatus] = useState(mc.status);

  let component = null;

  const handleStatusChange = () => {
    setStatus(chromecastStore.mediaStatus[device.uuid]);
  };

  chromecastStore.setCallback(device.uuid, handleStatusChange);

  if (mc.isPlaying) {
    const name = status.contentId.substring(status.contentId.lastIndexOf('/') + 1);
    component = (
      <div>
        <p>{name}</p>
        <TimeDisplay currentTime={status.currentTime} duration={status.duration} />
      </div>
    );
  }
  return (
    <Card title={device.name}>
      {component}
    </Card>
  );
};

export default ChromecastDeviceComponent;
