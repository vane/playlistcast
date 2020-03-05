import React, { useState } from 'react';
import moment from 'moment';
import momentDurationFormatSetup from 'moment-duration-format';
import { Card } from 'antd';
import chromecastStore from '../store/chromecastStore';

momentDurationFormatSetup(moment);

const timers = {};

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
        <TimeDisplay device={device} status={status} />
      </div>
    );
  }
  return (
    <Card title={device.name}>
      {component}
    </Card>
  );
};

const TimeDisplay = ({ device, status }) => {
  console.log('update', device, status.currentTime);
  const [currentTime, setCurrentTime] = useState(0);
  if (timers[device.uuid]) {
    console.log('clear');
    clearTimeout(timers[device.uuid]);
  }
  timers[device.uuid] = setTimeout(() => {
    if (status.currentTime > currentTime) {
      setCurrentTime(status.currentTime + 1);
    } else {
      setCurrentTime(currentTime + 1);
    }
  }, 1000);

  const current = moment.duration(currentTime, 'seconds').format('hh:mm:ss');
  const duration = moment.duration(status.duration, 'seconds').format('hh:mm:ss');
  return (
    <p>
      <span>{current}</span>
      <span>/</span>
      <span>{duration}</span>
    </p>
  );
};

export default ChromecastDeviceComponent;
