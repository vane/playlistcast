import React, { useState, useEffect } from 'react';
import { Button, Card } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlayCircle, faPauseCircle } from '@fortawesome/free-regular-svg-icons';
import chromecastStore from '../store/chromecastStore';
import TimeDisplay from './timeDisplay';
import { chromecastPause, chromecastPlay } from '../service/chromecast';


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

  useEffect(() => {
    const handleStatusChange = () => {
      setStatus(chromecastStore.mediaStatus[device.uuid]);
    };
    chromecastStore.setCallback(device.uuid, handleStatusChange);
    return () => chromecastStore.delCallback(device.uuid);
  });

  const handlePauseClick = () => {
    console.log('handlePauseClick');
    chromecastPause(device.uuid);
  };

  const handlePlayClick = () => {
    console.log('handlePlayClick');
    chromecastPlay(device.uuid);
  };

  let component = null;

  if (status.playerState === 'PLAYING') {
    const name = status.contentId.substring(status.contentId.lastIndexOf('/') + 1);
    component = (
      <div>
        <p>{name}</p>
        <TimeDisplay
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <Button type="link" icon={<FontAwesomeIcon icon={faPauseCircle} onClick={handlePauseClick} size="2x" />} />
      </div>
    );
  } else if (status.playerState === 'PAUSED') {
    const name = status.contentId.substring(status.contentId.lastIndexOf('/') + 1);
    component = (
      <div>
        <p>{name}</p>
        <TimeDisplay
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <Button type="link" icon={<FontAwesomeIcon icon={faPlayCircle} onClick={handlePlayClick} size="2x" />} />
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
