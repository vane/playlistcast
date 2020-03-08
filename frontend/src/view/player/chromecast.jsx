import React, { useState, useEffect } from 'react';
import { Button, Card } from 'antd';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlayCircle, faPauseCircle } from '@fortawesome/free-regular-svg-icons';
import { faVolumeUp } from '@fortawesome/free-solid-svg-icons';
import chromecastStore from '../../store/chromecastStore';
import { chromecastPause, chromecastPlay } from '../../service/chromecast';
import TimeDisplay from './timeDisplay';
import VolumeComponent from './volume';
import TimeProgressComponent from './timeProgress';

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
  const castStatus = device.status;
  const [status, setStatus] = useState(mc.status);
  const [volumeVisible, setVolumeVisible] = useState(false);

  useEffect(() => {
    const handleStatusChange = () => {
      setStatus(chromecastStore.mediaStatus[device.uuid]);
    };
    chromecastStore.setCallback(device.uuid, handleStatusChange);
    return () => chromecastStore.delCallback(device.uuid);
  });

  const handlePauseClick = () => {
    chromecastPause(device.uuid);
  };

  const handlePlayClick = () => {
    chromecastPlay(device.uuid);
  };

  const handleVolumeChange = () => {
    setVolumeVisible(!volumeVisible);
  };

  let playPauseButton = null;

  if (status.playerState === 'PLAYING') {
    playPauseButton = <Button type="link" icon={<FontAwesomeIcon icon={faPauseCircle} onClick={handlePauseClick} size="2x" />} />;
  } else if (status.playerState === 'PAUSED') {
    playPauseButton = <Button type="link" icon={<FontAwesomeIcon icon={faPlayCircle} onClick={handlePlayClick} size="2x" />} />;
  }

  let name = '';
  let component = null;
  if (status.contentId !== null) {
    name = status.contentId.substring(status.contentId.lastIndexOf('/') + 1);
    let volumeComponent = null;
    if (volumeVisible) {
      volumeComponent = <VolumeComponent uid={device.uuid} volumeLevel={castStatus.volumeLevel} />;
    }
    component = (
      <div>
        <TimeDisplay
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <TimeProgressComponent
          uid={device.uuid}
          currentTime={status.currentTime}
          duration={status.duration}
          playerState={status.playerState}
        />
        <div>
          <Button
            type="link"
            style={{ marginRight: '10px' }}
            icon={<FontAwesomeIcon icon={faVolumeUp} onClick={handleVolumeChange} size="2x" />}
          />
          {playPauseButton}
        </div>
        {volumeComponent}
      </div>
    );
  }
  return (
    <Card title={device.name}>
      <div>
        <p>{name}</p>
        {component}
      </div>
    </Card>
  );
};

export default ChromecastDeviceComponent;
